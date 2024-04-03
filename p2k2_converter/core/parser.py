import yaml
import logging
from openpyxl import load_workbook
from pathlib import Path
from collections import Counter
from typing import List, Tuple, Dict
from p2k2_converter.core.classes import Order, Buyer
from p2k2_converter.core.workflow import workflow_for_product
from p2k2_converter.pipeline import Pipeline
from p2k2_converter.pipeline.branch import Branch, BranchBuilder
from p2k2_converter.pipeline.source import XlsmSource


class Parser:
    def __init__(self, workbook_path: Path, config_file: str):
        self.__workbook_path = workbook_path
        try:
            self.__workbook = load_workbook(workbook_path, data_only=True)
        except FileNotFoundError:
            logging.error(f"Error: File {workbook_path} not found.")
            raise
        except Exception as e:
            logging.error(f"Error: {e}")
            raise

        self.__workflow_pipeline = Pipeline(source=XlsmSource(str(self.__workbook_path)))
        with open(config_file, "r") as file:
            self.__config_file = yaml.safe_load(file)

    def __create_workflow_for(self, product: str, row_number: int) -> Branch:
        """
        Create a workflow branch for the given product.
        Args:
            product: The string containing the name of the product
            row_number: The number of the row inside the excell file

        Returns:
            Return a branch containing a preconfigured workflow for the product in input.

        """
        args = (row_number, self.__config_file)
        strategy = workflow_for_product(product, *args)
        builder = BranchBuilder(f"{product}_WORKFLOW_{row_number}")

        builder.add_from_function(strategy.model_definition) \
            .add_from_function(strategy.profiles_definition) \
            .add_from_function(strategy.cuts_definition) \
            .add_from_function(strategy.machining_definition) \
            .add_from_function(strategy.translation_definition)

        return builder.build()

    def __define_workflows(self, cell_values: List) -> None:
        """
        Populate the workflow pipeline with the products found in the excell file. The workflow for each product should
        be described inside the configuration file.
        Args:
            cell_values: A list containing the name of the products that should be produced. This should be extracted
                         from the excell file in input.
        """
        product_counter = Counter(cell_values)
        for product, occurrences in product_counter.items():

            if product not in self.__config_file:
                logging.warning(f"Product {product} not found in the configuration file.")
                continue

            config = self.__config_file[product]
            target_worksheet = self.__workbook[config["worksheet"]]
            remaining_occurrences = occurrences

            configuration_range = f"{config['product-column']}{config['starting-row']}:" \
                                  f"{config['pieces-column']}{config['ending-row']}"

            for row in target_worksheet[configuration_range]:
                if remaining_occurrences == 0:
                    break
                name = row[0].value
                pieces = row[1].value

                if name == product:
                    logging.info(f"Creating workflow for {name} with {pieces} pieces.")
                    for _ in range(pieces):
                        self.__workflow_pipeline.add_branch(self.__create_workflow_for(name, row[0].row))
                        remaining_occurrences -= 1

    def __get_buyer_information(self) -> Buyer:
        """
        Retrieve the Buyer's information from the input excell file.

        Returns:
            An instance of  Buyer class containing the information of the buyer of the order
        """
        global_config = self.__config_file["GLOBALS"]
        buyer_config = global_config["buyer"]
        worksheet = self.__workbook[global_config["input-worksheet"]]

        info_column = buyer_config['column']

        full_name = worksheet[f"{info_column}{buyer_config['full-name-row']}"].value
        email = worksheet[f"{info_column}{buyer_config['email-row']}"].value
        phone = worksheet[f"{info_column}{buyer_config['telephone-row']}"].value
        cell_phone = worksheet[f"{info_column}{buyer_config['cellphone-row']}"].value
        address = worksheet[f"{info_column}{buyer_config['address-row']}"].value
        city = worksheet[f"{info_column}{buyer_config['city-row']}"].value

        return Buyer(full_name=full_name, email=email, phone=phone, cell_phone=cell_phone, address=address, city=city)

    def __calculate_bars_for_order(self, order: Order) -> Dict[str, Dict[str, Tuple[Tuple[int, int], ...]]]:
        """
        Calculate the number of bars needed for the order in input.
        The function will read the values from the table in the "available-bar-worksheet" worksheet inside the excell
        file and will calculate the number of bars needed for each model depending on the total length of the pieces to
        produce.
        Args:
            order: The order to be produced.

        Returns:
            A dictionary where each key is a profile code and each value is a tuple of tuples in which each one contains
            the length of the bar and the number of bars needed.
        """

        model_profile_cuts = {}
        for model in order.models:
            profile_cuts = {}
            for profile_code, profile in model.profiles.items():
                if profile_code not in profile_cuts:
                    profile_cuts[profile_code] = []
                profile_cuts[profile_code] += [cut.length for cut in profile.cuts]
            model_profile_cuts[model.name] = profile_cuts

        global_config = self.__config_file["GLOBALS"]
        bars_worksheet = self.__workbook[self.__config_file["GLOBALS"]["available-bar-worksheet"]]
        configuration_range = f"{global_config['width-column']}{global_config['starting-row-bar']}:" \
                              f"{global_config['pieces-column']}{global_config['ending-row-bar']}"

        global_bars_used = Counter()
        model_profile_bars = {}

        for model_name, profile_cuts in model_profile_cuts.items():
            profile_bars = {}
            for profile_code, cuts in profile_cuts.items():
                total_length = sum(cuts)
                bars = []
                for row in bars_worksheet[configuration_range]:
                    bar_length, available_bars = row[0].value, row[1].value
                    if bar_length is None or available_bars is None or available_bars == 0:
                        continue
                    while total_length > 0 and available_bars > global_bars_used[bar_length]:
                        pieces_used = min((total_length // bar_length) + 1, available_bars - global_bars_used[bar_length])
                        total_length -= pieces_used * bar_length
                        bars.append((bar_length, int(pieces_used)))
                        global_bars_used[bar_length] += pieces_used  # increase the global count of bars used

                    if total_length <= 0:
                        break

                if total_length > 0:
                    default_bar_length = global_config["default-bar-length"]
                    pieces_used = (total_length // default_bar_length) + 1
                    bars.append((default_bar_length, pieces_used))

                profile_bars[profile_code] = tuple(bars)

            model_profile_bars[model_name] = profile_bars

        return model_profile_bars

    def parse(self) -> Tuple[Dict[str, Dict[str, Tuple[Tuple[int, int], ...]]], Order]:
        """
        Executes the parse of the given excell file in input. This will extract the products from the configured
        input worksheet, build the workflow pipeline and executes it returning the order.

        Returns:
            The order to be translated in the p2k2 format.
        """
        global_config = self.__config_file["GLOBALS"]
        input_worksheet = self.__workbook[global_config["input-worksheet"]]
        product_range = f"{global_config['product-column']}{global_config['starting-row']}:" \
                        f"{global_config['product-column']}{global_config['ending-row']}"

        values = [cell.value for row in input_worksheet[product_range] for cell in row if cell.value is not None]
        self.__define_workflows(values)
        self.__workflow_pipeline.execute()

        order = Order(buyer=self.__get_buyer_information())
        for model in self.__workflow_pipeline.get_branches_result():
            order.models.append(model)

        self.__calculate_bars_for_order(order)

        return self.__calculate_bars_for_order(order), order


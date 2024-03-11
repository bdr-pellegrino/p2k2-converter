import yaml
import logging
from openpyxl import load_workbook
from pathlib import Path
from collections import Counter
from typing import List
from p2k2_converter.config import WORKFLOW_CLASS_CONFIG
from p2k2_converter.core.classes import Order, Buyer
from p2k2_converter.pipeline import Pipeline
from p2k2_converter.pipeline.branch import Branch, BranchBuilder
from p2k2_converter.pipeline.source import XlsmSource
from p2k2_converter.core.workflow import Close


def get_workflow_class(product_name: str) -> str:
    """
    Dynamically instantiate the workflow class for the given product name.
    Is possible to bind a specific workflow class to a product using the work
    Args:
        product_name: The name of the product

    Returns:
        String containing the name of the class to instantiate
    """
    with open(str(WORKFLOW_CLASS_CONFIG), "r") as file:
        config = yaml.safe_load(file)
        for product in config["WORKFLOWS"]:
            if product_name in product["name"]:
                return product["class name"]

        raise ValueError(f"Product {product_name} not found in the configuration file.")


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
        class_name = get_workflow_class(product)
        dynamic_class = globals()[class_name]
        strategy = dynamic_class(row_number, self.__config_file)
        builder = BranchBuilder(f"{product}_WORKFLOW_{row_number}")

        builder.add_from_lambda("ModelDefinition", strategy.model_definition) \
            .add_from_lambda("ProfileDefinition", strategy.profiles_definition) \
            .add_from_lambda("BarsDefinition", strategy.cuts_definition) \
            .add_from_lambda("MachiningDefinition", strategy.machining_definition)

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

    def parse(self) -> Order:
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

        return order


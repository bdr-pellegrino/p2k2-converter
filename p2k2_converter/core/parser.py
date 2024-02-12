from openpyxl.workbook import Workbook

from p2k2_converter.core.workflow.workflow import Workflow
from p2k2_converter.pipeline import Pipeline
from p2k2_converter.pipeline.branch import Branch, BranchBuilder
from collections import Counter
import yaml
import logging


class Parser:
    def __init__(self, workbook: Workbook, config_file: str):
        self.__workflow_map = {
            "CLOSE": None
        }
        self.__workbook = workbook
        self.__workflow_pipeline = Pipeline()

        with open(config_file, "r") as file:
            self.__config_file = yaml.safe_load(file)

    def __create_workflow_for(self, product: str, row_number: int) -> Branch:
        strategy = Workflow(row_number, self.__config_file, product)
        builder = BranchBuilder(f"{product}_WORKFLOW")

        builder.add_from_lambda("ModelDefinition", strategy.model_definition) \
            .add_from_lambda("ProfileDefinition", strategy.profiles_definition) \
            .add_from_lambda("BarsDefinition", strategy.bars_definition) \
            .add_from_lambda("MachiningDefinition", strategy.machining_definition)

        return builder.build()

    def parse(self):
        global_config = self.__config_file["GLOBALS"]
        input_worksheet = self.__workbook[global_config["input-worksheet"]]
        product_range = f"{global_config['product-column']}{global_config['starting-row']}:" \
                        f"{global_config['product-column']}{global_config['ending-row']}"

        values = [cell.value for row in input_worksheet[product_range] for cell in row if cell.value is not None]

        product_counter = Counter(values)
        for product, occurrences in product_counter.items():
            logging.info(f"Creating workflow for {product} with {occurrences} occurrences.")

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




from p2k2_converter.pipeline import Pipeline
from p2k2_converter.pipeline.branch import Branch, BranchBuilder


class Parser:
    def __init__(self):
        self.__workflow_map = {
            "CLOSE": None
        }
        self.__workflow_pipeline = Pipeline()

    def create_workflow_for(self, product: str) -> Branch:
        strategy = self.__workflow_map[product]
        builder = BranchBuilder(f"{product}_WORKFLOW")

        builder.add_from_lambda("ModelDefinition", strategy.model_definition) \
               .add_from_lambda("ProfileDefinition", strategy.profiles_definition) \
               .add_from_lambda("BarsDefinition", strategy.bars_definition) \
               .add_from_lambda("MachiningDefinition", strategy.machining_definition)

        return builder.build()

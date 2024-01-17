from .base_step import BaseStep


class DataExtractor(BaseStep):
    def __init__(self, name: str, source=None):
        super().__init__(name)
        self.__source = source

    def set_data(self, source):
        """
        Sets the source to be used in this step
        """
        self.__source = source

    def extract_data(self):
        """
        Extracts data from the source
        """
        pass




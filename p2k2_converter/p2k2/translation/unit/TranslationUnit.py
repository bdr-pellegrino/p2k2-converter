
class TranslationUnit:
    def __init__(self):
        self.__translation_strategy = None

    def set_translation_strategy(self, strategy):
        """
        Set the translation strategy

        Args:
            strategy (function): The translation strategy
        """
        self.__translation_strategy = strategy

    def translate(self):
        """
        Convert the internal data in the p2k2 format

        Returns:
            A configured p2k2 class
        """
        if self.__translation_strategy is None:
            raise NotImplementedError("Translation strategy not defined")

        return self.__translation_strategy()

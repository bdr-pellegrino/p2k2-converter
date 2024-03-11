from abc import ABC, abstractmethod


class TranslationUnit(ABC):

    @abstractmethod
    def translate(self):
        """
        Convert the internal data in the p2k2 format

        Returns:
            A configured p2k2 class
        """
        pass

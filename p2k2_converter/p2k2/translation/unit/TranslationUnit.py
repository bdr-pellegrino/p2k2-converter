from abc import ABC, abstractmethod


class TranslationUnit(ABC):

    @abstractmethod
    def translate(self):
        """
        Convert the internal data in a p2k2 class.

        Returns:
            A configured p2k2 class
        """
        pass


from abc import ABC, abstractmethod


class WorkflowStrategy(ABC):

    @abstractmethod
    def model_definition(self, source, data):
        """
        Define the operations for creating a model for the product.

        Args:
            source: The source where the information is extracted
            data: The initial data
        """
        pass

    @abstractmethod
    def profiles_definition(self, source, model):
        """
        Define the profiles for a given model

        Args:
            source: The source where the information is extracted
            model: The target model

        """
        pass

    @abstractmethod
    def cuts_definition(self, source, model):
        """
        Define the cuts to be applied to the profiles

        Args:
            source: The source where the information is extracted
            model: The target model
        """
        pass

    @abstractmethod
    def machining_definition(self, source, model):
        """
        Define the machining to be applied to the profiles

        Args:
            source: The source where the information is extracted
            model: The target model
        """
        pass

    @abstractmethod
    def translation_definition(self, source, model):
        """
        Define the translation unit class for the following model.

        Args:
            source: The source where the information is extracted
            model: The target model
        """
        pass

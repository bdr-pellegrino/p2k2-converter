
from abc import ABC, abstractmethod


class WorkflowStrategy(ABC):

    @abstractmethod
    def model_definition(self, source, data):
        pass

    @abstractmethod
    def profiles_definition(self, source, data):
        pass

    @abstractmethod
    def cuts_definition(self, source, data):
        pass

    @abstractmethod
    def machining_definition(self, source, data):
        pass

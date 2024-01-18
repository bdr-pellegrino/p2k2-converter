from typing import TypeVar
from abc import ABC, abstractmethod
from contextlib import contextmanager

T = TypeVar('T')


class BaseSource(ABC):

    @abstractmethod
    @contextmanager
    def open(self) -> T:
        pass

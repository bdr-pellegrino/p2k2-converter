from typing import TypeVar
from contextlib import contextmanager
from abc import ABC, abstractmethod

T = TypeVar('T')


class BaseSource(ABC):
    @contextmanager
    @abstractmethod
    def open(self) -> T:
        pass

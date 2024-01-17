from typing import TypeVar
from contextlib import contextmanager

T = TypeVar('T')


class BaseSource:
    @contextmanager
    def open(self) -> T:
        pass

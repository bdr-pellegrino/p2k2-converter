from typing import TypeVar

T = TypeVar('T')

class BaseSource:

    def open(self) -> T:
        ...


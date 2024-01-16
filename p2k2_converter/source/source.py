from typing import TypeVar

T = TypeVar("T")


class Source:

    def open(self) -> T:
        """
        Opens the source and returns the object used to read from it.
        """
        ...

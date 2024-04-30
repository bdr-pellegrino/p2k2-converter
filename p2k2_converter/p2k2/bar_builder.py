from typing import List
from p2k2_converter.p2k2.classes import Cut, Sfrido, Bar


class BarBuilder:

    def __init__(self, brand: str, system: str, profile_code: str):
        self.__bars_cut_together = 1
        self.__height = None
        self.__off_cut = None
        self.__remaining_length = None
        self.__length = None
        self.__brand = brand
        self.__system = system
        self.__profile_code = profile_code
        self.__cuts = []
        self.__outer_color = "STD"
        self.__inner_color = "STD"

    def add_inner_color(self, inner_color: str) -> 'BarBuilder':
        """
        Specify the inner color of the bar

        Args:
            inner_color: The code of the inner color

        Returns:
            The builder instance
        """
        self.__inner_color = inner_color
        return self

    def add_outer_color(self, outer_color: str) -> 'BarBuilder':
        """
        Specify the outer color of the bar

        Args:
            outer_color: the code of the outer color

        Returns:
            The builder instance
        """
        self.__outer_color = outer_color
        return self

    def add_length(self, length: float) -> 'BarBuilder':
        """
        Specify the length of the used bar

        Args:
            length: The length of the bar in millimeters

        Returns:
            The builder instance

        """
        self.__length = length
        return self

    def add_remaining_length(self, remaining_length: float) -> 'BarBuilder':
        """
        Specify the remaining length of the bar

        Args:
            remaining_length: The remaining length of the bar in millimeters

        Returns:
            The builder instance

        """
        self.__remaining_length = remaining_length
        return self

    def add_height(self, height: int) -> 'BarBuilder':
        """
        Specify the height of the bar

        Args:
            height: The height of the bar in millimeters

        Returns:
            The builder instance
        """
        self.__height = height
        return self

    def add_bars_cut_together(self, bars_cut_together: int) -> 'BarBuilder':
        """
        Specify the number of bar that are cut together

        Args:
            bars_cut_together: The number of bars cuts together, usually 1.

        Returns:
            The builder instance
        """
        self.__bars_cut_together = bars_cut_together
        return self

    def add_cut(self, cut: Cut) -> 'BarBuilder':
        """
        Add a cut to the bar

        Args:
            cut: A cut class that should be inserted in the bar

        Returns:
            The builder instance
        """
        self.__cuts.append(cut)
        return self

    def add_cuts(self, cuts: List[Cut]) -> 'BarBuilder':
        """
        Add a list of cuts to the bar

        Args:
            cuts: A list of cuts that should be inserted in the bar

        Returns:
            The builder instance
        """
        self.__cuts += cuts
        return self

    def add_off_cut(self, code: str, trolley: int, slot: int) -> 'BarBuilder':
        """
        Add an off cut (Sfrido) in the bar

        Args:
            code: The off cut code
            trolley: The trolley
            slot: The slot

        Returns:
            The builder instance
        """
        self.__off_cut = Sfrido(code, trolley, slot)
        return self

    def build(self) -> 'Bar':
        """
        Build an instance of the bar with the information collected.

        Returns:
            An instance of a Bar

        """
        if len(self.__cuts) == 0:
            raise ValueError(f"No cuts added to with brand {self.__brand}, system {self.__system} and code {self.__profile_code}.")

        if self.__length is None:
            raise ValueError("No length added to bar")

        return Bar(
            bran=self.__brand,
            syst=self.__system,
            code=self.__profile_code,
            dicl=self.__inner_color,
            docl=self.__outer_color,
            len=self.__length,
            lenr=self.__remaining_length,
            h=self.__height,
            mlt=self.__bars_cut_together,
            cut=self.__cuts,
            sfrido=self.__off_cut
        )



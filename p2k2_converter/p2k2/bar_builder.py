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
        self.__inner_color = inner_color
        return self

    def add_outer_color(self, outer_color: str) -> 'BarBuilder':
        self.__outer_color = outer_color
        return self

    def add_length(self, length: float) -> 'BarBuilder':
        self.__length = length
        return self

    def add_remaining_length(self, remaining_length: float) -> 'BarBuilder':
        self.__remaining_length = remaining_length
        return self

    def add_height(self, height: int) -> 'BarBuilder':
        self.__height = height
        return self

    def add_bars_cut_together(self, bars_cut_together: int) -> 'BarBuilder':
        self.__bars_cut_together = bars_cut_together
        return self

    def add_cut(self, cut: Cut) -> 'BarBuilder':
        self.__cuts.append(cut)
        return self

    def add_off_cut(self, code: str, trolley: int, slot: int) -> 'BarBuilder':
        self.__off_cut = Sfrido(code, trolley, slot)
        return self

    def build(self) -> 'Bar':

        if len(self.__cuts) == 0:
            raise ValueError("No cuts added to bar")

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
            mlt=self.__bars_cut_together,
            h=self.__height,
            cut=self.__cuts,
            sfrido=self.__off_cut
        )



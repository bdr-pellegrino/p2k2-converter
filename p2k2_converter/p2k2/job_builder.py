from p2k2_converter.p2k2.classes import Job, Version, Bar, Pdat, Body, Head


class JobBuilder:
    def __init__(self, version: Version = Version(mj=1, mn=0)):
        self.__version = version
        self.__bars = []
        self.__pdat = []

    def add_pdat(self, code: str, internal_color_code: str,
                 external_color_code: str, bar_quantity: int) -> 'JobBuilder':
        self.__pdat.append(Pdat(code, internal_color_code, external_color_code, bar_quantity))
        return self

    def add_bar(self, bar: Bar) -> 'JobBuilder':
        self.__bars.append(bar)
        return self

    def build(self) -> Job:
        if len(self.__bars) == 0:
            raise ValueError("No bars added to job")

        version = self.__version
        head = Head(self.__pdat) if len(self.__pdat) > 0 else None
        body = Body(self.__bars)
        return Job(version, head, body)

from p2k2_converter.p2k2.classes import Cut, Machining, Machinings, Forbiddenspace


class CutBuilder:
    def __init__(self):
        self.__trolley_code = None
        self.__trolley_slot_code = None
        self.__stop_code = None
        self.__area = None
        self.__bar_code = None
        self.__exit_number = None
        self.__square_number = None
        self.__customer_name = None
        self.__typology = None
        self.__order_code = None
        self.__right_trim_cut_angle = None
        self.__left_trim_cut_angle = None
        self.__right_trim_cut_length = None
        self.__left_trim_cut_length = None
        self.__inferior_cut_length = None
        self.__superior_cut_length = None
        self.__right_beta_cutting_angle = None
        self.__right_cutting_angle = None
        self.__left_cutting_angle = None
        self.__left_beta_cutting_angle = None
        self.__labels = []
        self.__machinings = []
        self.__forbidden_spaces = []

    def add_left_cutting_angle(self, angle: int) -> 'CutBuilder':
        self.__left_cutting_angle = angle
        return self

    def add_right_cutting_angle(self, angle: int) -> 'CutBuilder':
        self.__right_cutting_angle = angle
        return self

    def add_right_beta_cutting_angle(self, angle: int) -> 'CutBuilder':
        self.__right_beta_cutting_angle = angle
        return self

    def add_left_beta_cutting_angle(self, angle: int) -> 'CutBuilder':
        self.__left_beta_cutting_angle = angle
        return self

    def add_cut_length(self, length: int) -> 'CutBuilder':
        self.add_superior_cut_length(length)
        self.add_inferior_cut_length(length)
        return self

    def add_superior_cut_length(self, length: int) -> 'CutBuilder':
        self.__superior_cut_length = length
        return self

    def add_inferior_cut_length(self, length: int) -> 'CutBuilder':
        self.__inferior_cut_length = length
        return self

    def add_left_trim_cut_length(self, length: int) -> 'CutBuilder':
        self.__left_trim_cut_length = length
        return self

    def add_right_trim_cut_length(self, length: int) -> 'CutBuilder':
        self.__right_trim_cut_length = length
        return self

    def add_left_trim_cut_angle(self, angle: int) -> 'CutBuilder':
        self.__left_trim_cut_angle = angle
        return self

    def add_right_trim_cut_angle(self, angle: int) -> 'CutBuilder':
        self.__right_trim_cut_angle = angle
        return self

    def add_order_code(self, code: str) -> 'CutBuilder':
        self.__order_code = code
        return self

    def add_typology(self, typology: str) -> 'CutBuilder':
        self.__typology = typology
        return self

    def add_customer_name(self, name: str) -> 'CutBuilder':
        self.__customer_name = name
        return self

    def add_square_number(self, number: str) -> 'CutBuilder':
        self.__square_number = number
        return self

    def add_bar_code(self, code: str) -> 'CutBuilder':
        self.__bar_code = code
        return self

    def add_label(self, label: str) -> 'CutBuilder':
        if len(self.__labels) < 4:
            self.__labels.append(label)
        else:
            raise ValueError("Max 4 labels allowed")
        return self

    def add_machining(self, code: str, offset: int, clamp_near: int = None) -> 'CutBuilder':
        self.__machinings.append(Machining(code, offset, clamp_near))
        return self

    def add_exit(self, exit_number: int) -> 'CutBuilder':
        self.__exit_number = exit_number
        return self

    def add_area(self, area: int) -> 'CutBuilder':
        self.__area = area
        return self

    def add_stop(self, stop_code: int) -> 'CutBuilder':
        self.__stop_code = stop_code
        return self

    def add_trolley(self, trolley_code: int) -> 'CutBuilder':
        self.__trolley_code = trolley_code
        return self

    def add_trolley_slot(self, trolley_slot_code: int) -> 'CutBuilder':
        self.__trolley_slot_code = trolley_slot_code
        return self

    def add_forbidden_space(self, start: int, end: int) -> 'CutBuilder':
        self.__forbidden_spaces.append(Forbiddenspace(start, end))
        return self

    def build(self) -> Cut:
        if self.__left_cutting_angle is None or self.__right_cutting_angle is None:
            raise ValueError("Cutting angles are both required for producing a cut")

        if self.__inferior_cut_length is None or self.__superior_cut_length is None:
            raise ValueError("Cutting lengths are both required for producing a cut")

        if len(self.__machinings) > 0:
            self.__machinings = Machinings(self.__machinings)

        return Cut(
            angl=self.__left_cutting_angle,
            angr=self.__right_cutting_angle,
            ab1=self.__left_beta_cutting_angle,
            ab2=self.__right_beta_cutting_angle,
            il=self.__inferior_cut_length,
            ol=self.__superior_cut_length,
            trml=self.__left_trim_cut_length,
            trmr=self.__right_trim_cut_length,
            tal=self.__left_trim_cut_angle,
            tar=self.__right_trim_cut_angle,
            orcd=self.__order_code,
            tina=self.__typology,
            csna=self.__customer_name,
            idquadro=self.__square_number,
            bcod=self.__bar_code,
            lbl=self.__labels,
            machinings=self.__machinings,
            exit=self.__exit_number,
            area=self.__area,
            stop=self.__stop_code,
            trolley=self.__trolley_code,
            slot=self.__trolley_slot_code,
            forbiddenspaces=self.__forbidden_spaces
        )

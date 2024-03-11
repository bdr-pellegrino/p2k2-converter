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
        """
        Insert the left cutting angle

        Args:
            angle: the measure of the angle using degrees

        Returns:
            The instance of the builder
        """
        self.__left_cutting_angle = angle
        return self

    def add_right_cutting_angle(self, angle: int) -> 'CutBuilder':
        """
        Specify the right cutting angle

        Args:
            angle: the measure of the angle using degrees

        Returns:
            The instance of the builder
        """
        self.__right_cutting_angle = angle
        return self

    def add_right_beta_cutting_angle(self, angle: int) -> 'CutBuilder':
        """
        Specify the right beta cutting angle

        Args:
            angle: the measure of the angle using degrees

        Returns:
            The instance of the builder
        """
        self.__right_beta_cutting_angle = angle
        return self

    def add_left_beta_cutting_angle(self, angle: int) -> 'CutBuilder':
        """
        Specify the left beta cutting angle

        Args:
            angle: the measure of the angle using degrees

        Returns:
            The instance of the builder
        """
        self.__left_beta_cutting_angle = angle
        return self

    def add_cut_length(self, length: float) -> 'CutBuilder':
        """
        Specify the length of a cut

        Args:
            length: the measure of the piece to be cut

        Returns:
            The instance of the builder
        """
        self.add_superior_cut_length(length)
        self.add_inferior_cut_length(length)
        return self

    def add_superior_cut_length(self, length: float) -> 'CutBuilder':
        """
        Specify the superior cut length of the piece

        Args:
            length: The superior length of the piece to be cut

        Returns:
            The instance of the builder
        """
        self.__superior_cut_length = length
        return self

    def add_inferior_cut_length(self, length: float) -> 'CutBuilder':
        """
        Specify the inferior cut length of the piece

        Args:
            length: The inferior length of the piece to be cut

        Returns:
            The instance of the builder
        """
        self.__inferior_cut_length = length
        return self

    def add_left_trim_cut_length(self, length: int) -> 'CutBuilder':
        """
        Specify the left trim cut length of the piece

        Args:
            length: The left trim cut length of the piece

        Returns:
            The instance of the builder
        """
        self.__left_trim_cut_length = length
        return self

    def add_right_trim_cut_length(self, length: int) -> 'CutBuilder':
        """
        Specify the right trim cut length of the piece

        Args:
            length: The right trim cut length of the piece

        Returns:
            The instance of the builder
        """
        self.__right_trim_cut_length = length
        return self

    def add_left_trim_cut_angle(self, angle: int) -> 'CutBuilder':
        """
        Specify the left trim cut angle of the piece

        Args:
            angle: The right trim cut angle of the piece

        Returns:
            The instance of the builder
        """
        self.__left_trim_cut_angle = angle
        return self

    def add_right_trim_cut_angle(self, angle: int) -> 'CutBuilder':
        """
        Specify the right trim cut angle of the piece

        Args:
            angle: The right trim cut angle of the piece

        Returns:
            The instance of the builder
        """
        self.__right_trim_cut_angle = angle
        return self

    def add_order_code(self, code: str) -> 'CutBuilder':
        """
        Specify the order code associated with this piece

        Args:
            code: The code associated with this piece

        Returns:
            The instance of the builder
        """
        self.__order_code = code
        return self

    def add_typology(self, typology: str) -> 'CutBuilder':
        """
        Specify the typology code associated with this piece

        Args:
            typology: The typology of this piece

        Returns:
            The instance of the builder
        """
        self.__typology = typology
        return self

    def add_customer_name(self, name: str) -> 'CutBuilder':
        """
        Specify the customer name

        Args:
            name: Name of the customer

        Returns:
            The instance of the builder
        """
        self.__customer_name = name
        return self

    def add_square_number(self, number: str) -> 'CutBuilder':
        """
        Specify the square number ("idquadro") of the piece

        Args:
            number: The square number

        Returns:
            The instance of the builder
        """
        self.__square_number = number
        return self

    def add_bar_code(self, code: str) -> 'CutBuilder':
        """
        Specify the barcode of the piece

        Args:
            code: the barcode

        Returns:
            The instance of the builder
        """
        self.__bar_code = code
        return self

    def add_label(self, label: str) -> 'CutBuilder':
        """
        Specify a label for this piece.
        Only four labels are allowed for each piece

        Args:
            label: The content of the label

        Returns:
            The instance of the builder
        """
        if len(self.__labels) < 4:
            self.__labels.append(label)
        else:
            raise ValueError("Max 4 labels allowed")
        return self

    def add_machining(self, code: str, offset: float, clamp_near: int = None) -> 'CutBuilder':
        """
        Specify a machining for this piece.

        Args:
            code: The machining code
            offset: The offset where the machining should be applied
            clamp_near: The clamp near value (default to None)

        Returns:
            The instance of the builder
        """
        self.__machinings.append(Machining(code, offset, clamp_near))
        return self

    def add_exit(self, exit_number: int) -> 'CutBuilder':
        """
        Specify the exit for this piece

        Args:
            exit_number: The exit number of the machine

        Returns:
            The instance of the builder
        """
        self.__exit_number = exit_number
        return self

    def add_area(self, area: int) -> 'CutBuilder':
        """
        Specify the area number for this piece


        Args:
            area: The area number of the piece

        Returns:
            The instance of the builder
        """
        self.__area = area
        return self

    def add_stop(self, stop_code: int) -> 'CutBuilder':
        """
        Specify a stop code for this piece

        Args:
            stop_code: The stop code

        Returns:
            The instance of the builder
        """
        self.__stop_code = stop_code
        return self

    def add_trolley(self, trolley_code: int) -> 'CutBuilder':
        """
        Specify a trolley for the piece

        Args:
            trolley_code: The specific code of the trolley to use

        Returns:
            The instance of the builder

        """
        self.__trolley_code = trolley_code
        return self

    def add_trolley_slot(self, trolley_slot_code: int) -> 'CutBuilder':
        """
        Specify the trolley slot

        Args:
            trolley_slot_code: The trolley slot code

        Returns:
            The instance of the builder
        """
        self.__trolley_slot_code = trolley_slot_code
        return self

    def add_forbidden_space(self, start: int, end: int) -> 'CutBuilder':
        """
        Specify a forbidden space for the piece.

        Args:
            start: The starting offset of the forbidden space
            end: The ending offset of the forbidden space

        Returns:
            The instance of the builder
        """
        self.__forbidden_spaces.append(Forbiddenspace(start, end))
        return self

    def build(self) -> Cut:
        """
        Build an instance of the cut with the information collected.

        Returns:
            An instance of a Cut
        """
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

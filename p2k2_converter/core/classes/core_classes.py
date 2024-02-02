from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Buyer:
    full_name: Optional[str] = field(
        metadata={"description": "Full name of the buyer"}
    )

    email: Optional[str] = field(
        metadata={"description": "Email of the buyer"}
    )

    phone: Optional[str] = field(
        metadata={"description": "Phone number of the buyer"}
    )

    cell_phone: Optional[str] = field(
        metadata={"description": "Cell phone number of the buyer"}

    )
    address: Optional[str] = field(
        metadata={"description": "Address of the buyer"}
    )

    city: Optional[str] = field(
        metadata={"description": "City of the buyer"}
    )

    zip: Optional[str] = field(
        metadata={"description": "Zip code of the buyer"}
    )

    country: Optional[str] = field(
        metadata={"description": "Country of the buyer"}
    )


@dataclass
class ModelOptional:
    name: Optional[str] = field(
        metadata={"description": "Name of the optional"}
    )


@dataclass
class Machining:
    code: Optional[str] = field(
        metadata={"description": "Code of the machining"}
    )


@dataclass
class Bar:
    serial_code: Optional[str] = field(
        metadata={"description": "Serial code of the bar"}
    )
    length: Optional[float] = field(
        metadata={"description": "Length of the bar"}
    )


@dataclass
class Cut:
    length: Optional[float] = field(
        metadata={"description": "Length of the cut"}
    )
    angleL: Optional[int] = field(
        default=90,
        metadata={"description": "Left cut angle"}
    )

    angleR: Optional[int] = field(
        default=90,
        metadata={"description": "Right cut angle"}
    )


@dataclass
class Profile:
    system: str = field(
        metadata={"description": "System of the profile"}
    )
    code: str = field(
        metadata={"description": "Code of the profile"}
    )
    refinement: Optional[float] = field(
        metadata={"description": "The refinement to be applied to the profile that is being produced"}
    )
    machinings: List[Machining] = field(
        default_factory=list,
        metadata={"description": "Machining to be applied to the profile"}
    )
    bars: List[Bar] = field(
        default_factory=list,
        metadata={"description": "List of bars being used for producing this profile"}
    )
    brand: str = field(
        default="PELLEGRINO",
        metadata={"description": "Brand of the profile"}
    )


@dataclass
class Model:
    name: str = field(
        metadata={"description": "Name of the model"}
    )
    width: float = field(
        metadata={"description": "Width of the model"}
    )
    height: float = field(
        metadata={"description": "Height of the model"}
    )
    optionals: List[ModelOptional] = field(
        default_factory=list,
        metadata={"description": "List of optionals to be applied to the model"}
    )
    profiles: List[Profile] = field(
        default_factory=list,
        metadata={"description": "List of profiles being used for producing this model"}
    )


@dataclass
class Order:
    buyer: Optional[Buyer] = field(
        metadata={"description": "Buyer of the order"}
    )
    models: List[Model] = field(
        default_factory=list,
        metadata={"description": "List of models being ordered"}
    )


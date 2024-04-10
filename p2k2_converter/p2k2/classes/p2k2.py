from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Forbiddenspace:
    class Meta:
        name = "FORBIDDENSPACE"

    start: Optional[int] = field(
        default=None,
        metadata={
            "name": "START",
            "type": "Attribute",
        }
    )
    end: Optional[int] = field(
        default=None,
        metadata={
            "name": "END",
            "type": "Attribute",
        }
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


@dataclass
class Machining:
    class Meta:
        name = "MACHINING"

    wcode: Optional[str] = field(
        default=None,
        metadata={
            "name": "WCODE",
            "type": "Attribute",
        }
    )
    offset: Optional[float] = field(
        default=None,
        metadata={
            "name": "OFFSET",
            "type": "Attribute",
        }
    )
    clampnear: Optional[int] = field(
        default=None,
        metadata={
            "name": "CLAMPNEAR",
            "type": "Attribute",
        }
    )


@dataclass
class Pdat:
    class Meta:
        name = "PDAT"

    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CODE",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    dicl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DICL",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    docl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DOCL",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    bqty: Optional[int] = field(
        default=None,
        metadata={
            "name": "BQTY",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )


@dataclass
class Sfrido:
    class Meta:
        name = "SFRIDO"

    idxpezzo: Optional[str] = field(
        default=None,
        metadata={
            "name": "IDXPEZZO",
            "type": "Element",
            "namespace": "",
        }
    )
    trolley: Optional[int] = field(
        default=None,
        metadata={
            "name": "TROLLEY",
            "type": "Element",
            "namespace": "",
        }
    )
    slot: Optional[int] = field(
        default=None,
        metadata={
            "name": "SLOT",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Version:
    class Meta:
        name = "VERSION"

    mj: Optional[int] = field(
        default=None,
        metadata={
            "name": "MJ",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    mn: Optional[int] = field(
        default=None,
        metadata={
            "name": "MN",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )


@dataclass
class Forbiddenspaces:
    class Meta:
        name = "FORBIDDENSPACES"

    forbiddenspace: List[Forbiddenspace] = field(
        default_factory=list,
        metadata={
            "name": "FORBIDDENSPACE",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Head:
    class Meta:
        name = "HEAD"

    pdat: List[Pdat] = field(
        default_factory=list,
        metadata={
            "name": "PDAT",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        }
    )


@dataclass
class Machinings:
    class Meta:
        name = "MACHININGS"

    machining: List[Machining] = field(
        default_factory=list,
        metadata={
            "name": "MACHINING",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Cut:
    class Meta:
        name = "CUT"

    angl: Optional[int] = field(
        default=None,
        metadata={
            "name": "ANGL",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    angr: Optional[int] = field(
        default=None,
        metadata={
            "name": "ANGR",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    ab1: Optional[int] = field(
        default=None,
        metadata={
            "name": "AB1",
            "type": "Element",
            "namespace": "",
        }
    )
    ab2: Optional[int] = field(
        default=None,
        metadata={
            "name": "AB2",
            "type": "Element",
            "namespace": "",
        }
    )
    il: Optional[int] = field(
        default=None,
        metadata={
            "name": "IL",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    ol: Optional[int] = field(
        default=None,
        metadata={
            "name": "OL",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    trml: Optional[int] = field(
        default=None,
        metadata={
            "name": "TRML",
            "type": "Element",
            "namespace": "",
        }
    )
    trmr: Optional[int] = field(
        default=None,
        metadata={
            "name": "TRMR",
            "type": "Element",
            "namespace": "",
        }
    )
    tal: Optional[int] = field(
        default=None,
        metadata={
            "name": "TAL",
            "type": "Element",
            "namespace": "",
        }
    )
    tar: Optional[int] = field(
        default=None,
        metadata={
            "name": "TAR",
            "type": "Element",
            "namespace": "",
        }
    )
    orcd: Optional[str] = field(
        default=None,
        metadata={
            "name": "ORCD",
            "type": "Element",
            "namespace": "",
        }
    )
    tina: Optional[str] = field(
        default=None,
        metadata={
            "name": "TINA",
            "type": "Element",
            "namespace": "",
        }
    )
    csna: Optional[str] = field(
        default=None,
        metadata={
            "name": "CSNA",
            "type": "Element",
            "namespace": "",
        }
    )
    idquadro: Optional[str] = field(
        default=None,
        metadata={
            "name": "IDQUADRO",
            "type": "Element",
            "namespace": "",
        }
    )
    bcod: Optional[str] = field(
        default=None,
        metadata={
            "name": "BCOD",
            "type": "Element",
            "namespace": "",
        }
    )
    lbl: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LBL",
            "type": "Element",
            "namespace": "",
            "max_occurs": 4,
        }
    )
    machinings: Optional["Machinings"] = field(
        default=None,
        metadata={
            "name": "MACHININGS",
            "type": "Element",
            "namespace": "",
        }
    )
    cut: Optional["Cut"] = field(
        default=None,
        metadata={
            "name": "CUT",
            "type": "Element",
            "namespace": "",
        }
    )
    exit: Optional[int] = field(
        default=None,
        metadata={
            "name": "EXIT",
            "type": "Element",
            "namespace": "",
        }
    )
    area: Optional[int] = field(
        default=None,
        metadata={
            "name": "AREA",
            "type": "Element",
            "namespace": "",
            "min_inclusive": 1,
            "max_inclusive": 2,
        }
    )
    stop: Optional[int] = field(
        default=None,
        metadata={
            "name": "STOP",
            "type": "Element",
            "namespace": "",
        }
    )
    trolley: Optional[int] = field(
        default=None,
        metadata={
            "name": "TROLLEY",
            "type": "Element",
            "namespace": "",
        }
    )
    slot: Optional[int] = field(
        default=None,
        metadata={
            "name": "SLOT",
            "type": "Element",
            "namespace": "",
        }
    )
    forbiddenspaces: List[Forbiddenspaces] = field(
        default_factory=list,
        metadata={
            "name": "FORBIDDENSPACES",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Bar:
    class Meta:
        name = "BAR"

    bran: Optional[str] = field(
        default=None,
        metadata={
            "name": "BRAN",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    syst: Optional[str] = field(
        default=None,
        metadata={
            "name": "SYST",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CODE",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    dicl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DICL",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    docl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DOCL",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    len: Optional[int] = field(
        default=None,
        metadata={
            "name": "LEN",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    lenr: Optional[int] = field(
        default=None,
        metadata={
            "name": "LENR",
            "type": "Element",
            "namespace": "",
        }
    )
    h: Optional[int] = field(
        default=None,
        metadata={
            "name": "H",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    mlt: Optional[int] = field(
        default=None,
        metadata={
            "name": "MLT",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    cut: List[Cut] = field(
        default_factory=list,
        metadata={
            "name": "CUT",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        }
    )
    sfrido: Optional[Sfrido] = field(
        default=None,
        metadata={
            "name": "SFRIDO",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Body:
    class Meta:
        name = "BODY"

    bar: List[Bar] = field(
        default_factory=list,
        metadata={
            "name": "BAR",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        }
    )


@dataclass
class Job:
    class Meta:
        name = "JOB"

    ver: Optional[Version] = field(
        default=None,
        metadata={
            "name": "VER",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    head: Optional[Head] = field(
        default=None,
        metadata={
            "name": "HEAD",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    body: Optional[Body] = field(
        default=None,
        metadata={
            "name": "BODY",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )

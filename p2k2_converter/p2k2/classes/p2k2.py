from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "org.unibo.p2k2"


@dataclass
class Forbiddenspace:
    class Meta:
        name = "forbiddenspace"

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


@dataclass
class Machining:
    class Meta:
        name = "machining"

    wcode: Optional[str] = field(
        default=None,
        metadata={
            "name": "WCODE",
            "type": "Attribute",
        }
    )
    offset: Optional[int] = field(
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
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )


@dataclass
class Pdat:
    class Meta:
        name = "pdat"

    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CODE",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    dicl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DICL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    docl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DOCL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    bqty: Optional[int] = field(
        default=None,
        metadata={
            "name": "BQTY",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )


@dataclass
class Sfrido:
    class Meta:
        name = "sfrido"

    idxpezzo: List[str] = field(
        default_factory=list,
        metadata={
            "name": "IDXPEZZO",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    trolley: List[int] = field(
        default_factory=list,
        metadata={
            "name": "TROLLEY",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    slot: List[int] = field(
        default_factory=list,
        metadata={
            "name": "SLOT",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )


@dataclass
class Version:
    class Meta:
        name = "version"

    mj: Optional[int] = field(
        default=None,
        metadata={
            "name": "MJ",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    mn: Optional[int] = field(
        default=None,
        metadata={
            "name": "MN",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )


@dataclass
class Forbiddenspaces:
    class Meta:
        name = "forbiddenspaces"

    forbiddenspace: List[Forbiddenspace] = field(
        default_factory=list,
        metadata={
            "name": "FORBIDDENSPACE",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )


@dataclass
class Head:
    class Meta:
        name = "head"

    pdat: List[Pdat] = field(
        default_factory=list,
        metadata={
            "name": "PDAT",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "min_occurs": 1,
        }
    )


@dataclass
class Machinings:
    class Meta:
        name = "machinings"

    machining: List[Machining] = field(
        default_factory=list,
        metadata={
            "name": "MACHINING",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )


@dataclass
class Cut:
    class Meta:
        name = "cut"

    angl: Optional[int] = field(
        default=None,
        metadata={
            "name": "ANGL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    angr: Optional[int] = field(
        default=None,
        metadata={
            "name": "ANGR",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    ab1: Optional[int] = field(
        default=None,
        metadata={
            "name": "AB1",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    ab2: Optional[int] = field(
        default=None,
        metadata={
            "name": "AB2",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    il: Optional[int] = field(
        default=None,
        metadata={
            "name": "IL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    ol: Optional[int] = field(
        default=None,
        metadata={
            "name": "OL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    trml: Optional[int] = field(
        default=None,
        metadata={
            "name": "TRML",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    trmr: Optional[int] = field(
        default=None,
        metadata={
            "name": "TRMR",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    tal: Optional[int] = field(
        default=None,
        metadata={
            "name": "TAL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    tar: Optional[int] = field(
        default=None,
        metadata={
            "name": "TAR",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    orcd: Optional[str] = field(
        default=None,
        metadata={
            "name": "ORCD",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    tina: Optional[str] = field(
        default=None,
        metadata={
            "name": "TINA",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    csna: Optional[str] = field(
        default=None,
        metadata={
            "name": "CSNA",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    idquadro: Optional[str] = field(
        default=None,
        metadata={
            "name": "IDQUADRO",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    bcod: Optional[str] = field(
        default=None,
        metadata={
            "name": "BCOD",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    lbl: List[str] = field(
        default_factory=list,
        metadata={
            "name": "LBL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "max_occurs": 4,
        }
    )
    machinings: List[Machinings] = field(
        default_factory=list,
        metadata={
            "name": "MACHININGS",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    cut: Optional["Cut"] = field(
        default=None,
        metadata={
            "name": "CUT",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    exit: Optional[int] = field(
        default=None,
        metadata={
            "name": "EXIT",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    area: Optional[int] = field(
        default=None,
        metadata={
            "name": "AREA",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "min_inclusive": 1,
            "max_inclusive": 2,
        }
    )
    stop: Optional[int] = field(
        default=None,
        metadata={
            "name": "STOP",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    trolley: Optional[int] = field(
        default=None,
        metadata={
            "name": "TROLLEY",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    slot: Optional[int] = field(
        default=None,
        metadata={
            "name": "SLOT",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    forbiddenspaces: List[Forbiddenspaces] = field(
        default_factory=list,
        metadata={
            "name": "FORBIDDENSPACES",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )


@dataclass
class Bar:
    class Meta:
        name = "bar"

    bran: Optional[str] = field(
        default=None,
        metadata={
            "name": "BRAN",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    syst: Optional[str] = field(
        default=None,
        metadata={
            "name": "SYST",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "CODE",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    dicl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DICL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    docl: Optional[str] = field(
        default=None,
        metadata={
            "name": "DOCL",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    len: Optional[int] = field(
        default=None,
        metadata={
            "name": "LEN",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    lenr: Optional[int] = field(
        default=None,
        metadata={
            "name": "LENR",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )
    h: Optional[int] = field(
        default=None,
        metadata={
            "name": "H",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    mlt: Optional[int] = field(
        default=None,
        metadata={
            "name": "MLT",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "required": True,
        }
    )
    cut: List[Cut] = field(
        default_factory=list,
        metadata={
            "name": "CUT",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "min_occurs": 1,
        }
    )
    sfrido: Optional[Sfrido] = field(
        default=None,
        metadata={
            "name": "SFRIDO",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
        }
    )


@dataclass
class Body:
    class Meta:
        name = "body"

    bar: List[Bar] = field(
        default_factory=list,
        metadata={
            "name": "BAR",
            "type": "Element",
            "namespace": "org.unibo.p2k2",
            "min_occurs": 1,
        }
    )


@dataclass
class Job:
    class Meta:
        name = "JOB"
        namespace = "org.unibo.p2k2"

    ver: Optional[Version] = field(
        default=None,
        metadata={
            "name": "VER",
            "type": "Element",
            "required": True,
        }
    )
    head: Optional[Head] = field(
        default=None,
        metadata={
            "name": "HEAD",
            "type": "Element",
            "required": True,
        }
    )
    body: Optional[Body] = field(
        default=None,
        metadata={
            "name": "BODY",
            "type": "Element",
            "required": True,
        }
    )

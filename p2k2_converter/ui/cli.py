import logging
from pathlib import Path

from xsdata.formats.dataclass.serializers.config import SerializerConfig

from p2k2_converter.core import Parser
from p2k2_converter.p2k2.translation import p2k2_translation
from xsdata.formats.dataclass.serializers import XmlSerializer


from p2k2_converter import xlsm_to_p2k2


def run_cli(args):
    if args.gui:
        print("This is the CLI. Please run without the -g flag.")
        exit(1)

    if args.file is None:
        print("Please provide a file to convert.")
        exit(1)

    file_to_convert = Path(args.file)
    if not file_to_convert.exists():
        print(f"The file {args.file} does not exist.")
        exit(1)

    xlsm_to_p2k2(file_to_convert, args.config, args.output if args.output is not None else Path(args.file).parent / f"output.xml")


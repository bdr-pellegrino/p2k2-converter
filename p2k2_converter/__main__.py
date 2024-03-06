import argparse
from pathlib import Path

from xsdata.formats.dataclass.serializers.config import SerializerConfig

from p2k2_converter.core import Parser
from p2k2_converter.config import DEFAULT_CONFIG
from p2k2_converter.p2k2.translator import Translator
from xsdata.formats.dataclass.serializers import XmlSerializer

parser = argparse.ArgumentParser(description='Converts a cut sheet file into a P2K2 file.')
parser.add_argument("-f", "--file", type=str, help="The cut sheet file to convert in xlsm format.")
parser.add_argument("-c", "--config", type=str, help="The configuration file to use.")
parser.add_argument("-o", "--output", type=str, help="The output file path.")

args = parser.parse_args()
config_path = args.config if args.config is not None else DEFAULT_CONFIG

if args.file is None:
    print("Please provide a file to convert.")
    exit(1)

file_to_convert = Path(args.file)
if not file_to_convert.exists():
    print(f"The file {args.file} does not exist.")
    exit(1)

file_parser = Parser(workbook_path=file_to_convert, config_file=config_path)
order = file_parser.parse()

job = Translator(config_file=config_path).p2k2_translation(order)

config = SerializerConfig(pretty_print=True)
serializer = XmlSerializer(config=config)

output_path = args.output if args.output is not None else Path(args.file).parent / "output.xml"
with open(output_path, "w") as file:
    file.write(serializer.render(job))


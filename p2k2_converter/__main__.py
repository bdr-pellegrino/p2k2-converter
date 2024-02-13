import argparse
from p2k2_converter.core import Parser
from pathlib import Path
from p2k2_converter.config import DEFAULT_CONFIG

parser = argparse.ArgumentParser(description='Converts a cut sheet file into a P2K2 file.')
parser.add_argument("-f", "--file", type=str, help="The cut sheet file to convert in xlsm format.")
parser.add_argument("-c", "--config", type=str, help="The configuration file to use.")
parser.add_argument("-o", "--output", type=str, help="The output file name.")

args = parser.parse_args()
config_path = args.config if args.config is not None else DEFAULT_CONFIG

file_parser = Parser(workbook_path=Path(args.file), config_file=config_path)
file_parser.parse()


# this is the main module of your app
# it is only required if your project must be runnable
# this is the script to be executed whenever some users writes `python -m p2k2_converter` on the command line, eg.
#x = p2k2_converter.MyClass().my_method()
#print(x)

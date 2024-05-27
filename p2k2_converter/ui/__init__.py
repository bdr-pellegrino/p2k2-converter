import argparse
from p2k2_converter.config import DEFAULT_CONFIG


parser = argparse.ArgumentParser(description='Converts a cut sheet file into a P2K2 file.')
parser.add_argument("-g", "--gui", action="store_true", help="Whether to run the GUI or not.", default=False, required=False)
parser.add_argument("-f", "--file", type=str, help="The cut sheet file to convert in xlsm format.")
parser.add_argument("-c", "--config", type=str, help="The configuration file to use.", default=DEFAULT_CONFIG)
parser.add_argument("-o", "--output", type=str, help="The output file path.")


def main():
    args = parser.parse_args()
    if args.gui:
        from p2k2_converter.ui.gui import run_gui
        run_gui(args)
    else:
        from p2k2_converter.ui.cli import run_cli
        run_cli(args)

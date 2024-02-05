import argparse
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

parser = argparse.ArgumentParser(description='Converts a cut sheet file into a P2K2 file.')
parser.add_argument("-f", "--file", type=str, help="The cut sheet file to convert in xlsm format.")
parser.add_argument("-o", "--output", type=str, help="The output file name.")

args = parser.parse_args()

path = args.file
try:
    wb = load_workbook(path)
except FileNotFoundError:
    print(f"Error: File {path} not found.")
    exit(1)
except InvalidFileException:
    print(f"Error: File {path} is not a valid xlsm file.")
    exit(1)

worksheet = wb['IMMISSIONE DATI']
#print(worksheet["I64:L79"])



# this is the main module of your app
# it is only required if your project must be runnable
# this is the script to be executed whenever some users writes `python -m p2k2_converter` on the command line, eg.
#x = p2k2_converter.MyClass().my_method()
#print(x)

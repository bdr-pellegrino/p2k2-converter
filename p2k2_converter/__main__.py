import p2k2_converter
import argparse

parser = argparse.ArgumentParser(description='Converts a cut sheet file into a P2K2 file.')
parser.add_argument("-f", "--file", type=str, help="The cut sheet file to convert in xlsm format.")
parser.add_argument("-t", "--type", type=str, help="The sheet type")
parser.add_argument("-o", "--output", type=str, help="The output file name.")

args = parser.parse_args()

# this is the main module of your app
# it is only required if your project must be runnable
# this is the script to be executed whenever some users writes `python -m p2k2_converter` on the command line, eg.
#x = p2k2_converter.MyClass().my_method()
#print(x)

import numpy as np
import argparse
from ast import literal_eval

###############################################################################
# Syntax:
#      python3 binGenerator.py --binRange (0, 1) --Num_bins 50
#
###############################################################################

############################# Data Input ######################################

# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--binRange',
                    default="(0, 1)",
                    help='Bin range as a tuple')
parser.add_argument('--Num_bins_plusOne',
                    default=100,
                    type=int,
                    help='Input an int = (number of desired bins + 1)')
args = parser.parse_args()

###############################################################################

# Evaluating xRange
try:
    tupX = literal_eval(args.binRange)
except (SyntaxError, ValueError):
    print("%s -> Invalid tuple format given" % args.binRange)

a = tupX[0]
b = tupX[1]

bins = np.linspace(a, b, args.Num_bins_plusOne)

print (bins.tolist())

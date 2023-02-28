#!/usr/bin/env python3

'''
Usage:

    python3 rCutoffFromReplica.py --dat_files=DIPC_CHOL-CHOL.xyRDF

Note:

    Calculates the mean radius cutoff to find the nearest species neighbor
    from given xy_rdf data file(s). 

    Input argument(s)  : 

        --dat_files  : A list of xy_rdf files of different replica of SAME
                       system.

    This script takes the xy_rdf data from the --dat_files and find the first
    maximum (provided it is above 1). Once first maxima is found, the minima
    right after the first max is determined to be the r cutoff. This r cutoff
    of is averaged over all the data files given and standard deviation is
    found. The output is printed out.

'''
import argparse
import numpy as np
import sys
from scipy.signal import argrelextrema

parser = argparse.ArgumentParser()
parser.add_argument
parser.add_argument("--dat_files",
                    dest="dataFiles",
                    help="List of xy_rdf files of different replica of SAME \
                    system",
                    nargs="+")
args = parser.parse_args()

inputDataFiles = args.dataFiles

file1 = np.loadtxt(inputDataFiles[0], dtype=float)
distance1 = file1[:, 0]
numFiles = len(inputDataFiles)
data = np.zeros((numFiles,))
fileCounter = 0

for file in inputDataFiles:
    xyRDFdata = np.loadtxt(file, dtype=float)

    if np.array_equal(xyRDFdata[:, 0], distance1):
        distance = xyRDFdata[:, 0]
        xyRDF = xyRDFdata[:, 1]
        maximaIndex = argrelextrema(xyRDF, np.greater)
        minimaIndex = argrelextrema(xyRDF, np.less)
        for index in range(len(maximaIndex[0])):
            if xyRDF[maximaIndex[0][index]] > 1:
                firstMaxima = distance[maximaIndex[0][index]]
                break

        for index in range(len(minimaIndex[0])):
            if distance[minimaIndex[0][index]] > firstMaxima:
                rCutoff = distance[minimaIndex[0][index]]
                break

        data[fileCounter] = rCutoff
        fileCounter += 1
    else:
        sys.exit("r distances are not same in xy_rdf files given")

avgRcutoff = np.mean(data)
stdRcutoff = np.std(data)

print(avgRcutoff, "\t", stdRcutoff)

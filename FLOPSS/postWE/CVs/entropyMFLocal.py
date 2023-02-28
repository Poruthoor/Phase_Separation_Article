#!/usr/bin/env python3
'''
Example:
    python3 entropyMFLocal.py --model "1DIPC.psf" --traj "fixed_1DIPC_100.dcd"
    --lipid_list "lipidList.dat" --bins 6 > 1DIPC.entropyMF
'''

# Importing functional modules
import loos
import loos.pyloos
import numpy as np
import argparse
import sys
import miscFuncs.loosFuncs as lf

parser = argparse.ArgumentParser()
parser.add_argument("--model",
                    dest="model",
                    help="Structure to use")
parser.add_argument("--traj",
                    dest="trajectory",
                    help="Trajectory to use")
parser.add_argument("--lipid_list",
                    dest="lipidsList",
                    help="List of lipids in the system")
parser.add_argument("--bins",
                    dest="numBins",
                    type=int,
                    help="Number of bins")
args = parser.parse_args()

# Parsing the arguments into variables
model = loos.createSystem(args.model)
trajectory = loos.pyloos.Trajectory(args.trajectory, model)
numBin = args.numBins

# Converting model into dictionary
lipidAGContainer = lf.segs2pyDicts(model, args.lipidsList)[0]
numLipidTypes = len(lipidAGContainer.keys())

# Printing out header for output file
header = "# " + " ".join(sys.argv)
header2 = "# Norm MF entropy\tUpper Leaflet MFS\tLower Leaflet MFS"
print(header)
print(header2)

# Iterating over the trajectory frames
for frame in trajectory:

    binRange = lf.bin2DRange(frame)

    # Defining np aray to store 2D histogram data for each
    hist2DUp = np.zeros((numLipidTypes, numBin, numBin))
    hist2DLo = np.zeros((numLipidTypes, numBin, numBin))
    xEdgeUp = np.zeros((numLipidTypes, numBin+1))
    yEdgeUp = np.zeros((numLipidTypes, numBin+1))
    xEdgeLo = np.zeros((numLipidTypes, numBin+1))
    yEdgeLo = np.zeros((numLipidTypes, numBin+1))

    # Defining np array to store lipid type counts for each leaflet
    lipidCountsUp = np.zeros((numLipidTypes,))
    lipidCountsLo = np.zeros((numLipidTypes,))

    # Initializing key Counter
    C = 0

    # Extracting lipids to calculate centroids from the container dict
    for key, value in lipidAGContainer.items():

        # Separating lipids(value) to leaflets
        Up, Lo = lf.leafletLipidSeparator(value)

        lipidCountsUp[C] = len(Up)
        lipidCountsLo[C] = len(Lo)

        # 2D binning
        hist2DUp[C], xEdgeUp[C], yEdgeUp[C] = lf.binning2D(Up,
                                                           numBin,
                                                           binRange)
        hist2DLo[C], xEdgeLo[C], yEdgeLo[C] = lf.binning2D(Lo,
                                                           numBin,
                                                           binRange)

        # Updating key Counter
        C += 1

    # Sanity Check
    assert lf.edgeCheck(xEdgeUp, numBin), 'x Bin edges are different \
            for different upper lipids within a frame'
    assert lf.edgeCheck(yEdgeUp, numBin), 'y Bin edges are different \
            for different upper lipids within a frame'
    assert lf.edgeCheck(xEdgeLo, numBin), 'x Bin edges are different \
            for different lower lipids within a frame'
    assert lf.edgeCheck(yEdgeLo, numBin), 'y Bin edges are different \
            for different lower lipids within a frame'

    entropyMFUpper = lf.shannonMFEntropyLocalNormalized(hist2DUp)
    entropyMFLower = lf.shannonMFEntropyLocalNormalized(hist2DLo)
    entropyMFAVG = 0.5*(np.add(entropyMFUpper, entropyMFLower))

    # Print outputs
    print(entropyMFAVG, "\t", entropyMFUpper, "\t", entropyMFLower)

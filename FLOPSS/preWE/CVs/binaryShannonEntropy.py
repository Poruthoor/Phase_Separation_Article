#!/usr/bin/env python3
'''
Example:
    python3 binaryShannonEntropy.py --model 1DIPC.psf
                                    --traj  fixed_1DIPC_100.dcd
                                    --lipid_list lipidList.dat
                                    --r rFile.dat
'''

# Importing functional modules
import loos
import loos.pyloos
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
parser.add_argument("--r_file",
                    dest="radius",
                    help="File consisitng of radius of local region")
args = parser.parse_args()

# Parsing the arguments into variables
model = loos.createSystem(args.model)
trajectory = loos.pyloos.Trajectory(args.trajectory, model)
rFile = args.radius

# Reading rFile
rFileLipids, rAvgLipids, rVarLipids = lf.rFileReader(rFile)

# Converting model into dictionary
lipidContainer, system, lipidList = lf.segs2pyDicts(model,
                                                    args.lipidsList)

# Sanity Check
if lipidList != rFileLipids:
    sys.exit("Lipids listed in --lipid_list and --r arguments are different.\n\
             The order in which lipids listed in both files must be same too!")

# Since we are considering A-A, B-B and A-B interactions, taking max of all.
radius = float(max(rAvgLipids))

# Printing out header for output file
header = "# " + " ".join(sys.argv)
header1 = "# radius\t" + str(radius)
header2 = "# Avg Binary Entropy\tUpper Leaflet BSE \
        \tLower Leaflet BSE\tlikeUp\tlikeLo\tunlikeUp\
        \tunlikeLo"
print(header)
print(header1)
print(header2)

# Iterating over the trajectory frames
for frame in trajectory:

    # Separating lipids(value) to leaflets
    Upper, Lower = lf.leafletLipidSeparator(system)

    binaryEntropyUp, likeUp, unlikeUp = lf.binaryShannonEntropy(frame,
                                                                Upper,
                                                                radius)
    binaryEntropyLo, likeLo, unlikeLo = lf.binaryShannonEntropy(frame,
                                                                Lower,
                                                                radius)

    binaryEntropyAVG = 0.5*(binaryEntropyLo + binaryEntropyUp)

    # Print outputs
    print(binaryEntropyAVG, "\t", binaryEntropyUp, "\t", binaryEntropyLo,
          "\t", likeUp, "\t", likeLo, "\t", unlikeUp, "\t", unlikeLo)

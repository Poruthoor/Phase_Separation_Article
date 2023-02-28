#!/usr/bin/env python3
'''
Example:
    python3 DBSCANanalysis.py --model 1DIPC.psf
                              --traj fixed_1DIPC_100.dcd
                              --lipid_list lipidListNoCHOL.dat
                              --r rFileNoChol.dat > test4
'''

# Importing functional modules
import loos
import loos.pyloos
import sys
import argparse
import numpy as np
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
numLipidTypes = len(lipidContainer.keys())

# Sanity Check
if lipidList != rFileLipids:
    sys.exit("Lipids listed in --lipid_list and --r arguments are different.\n\
             The order in which lipids listed in both files must be same too!")

# Printing out header for output file
headerList = []
for segID in lipidList:
    headerList.append(str(segID)+"-"+str(segID))

header = "# " + " ".join(sys.argv)
header2 = "# Individual Species Contribution :\t " + "\t".join(headerList)
header3 = "# weighted-Mean-cluster-lipid\t wStd-cluster-lipid\t\
        Silhouette Coefficent"

print(header)
print(header2)
print(header3)

#  localArea = math.pi*(radius)*(radius)

for frame in trajectory:

    box = frame.periodicBox()

    # Initializing key Counter
    C = 0
    avgClusterLipids = []
    stdClusterLipids = []
    numClusters = []
    silhouette_Coefficent = []

    # Extracting lipids to calculate centroids from the container dict
    for key, value in lipidContainer.items():

        # Collecting radius cutoff from rFile
        rCut = float(rAvgLipids[C])
        keyClusterLipids = []
        keyCoreLipids = []

        Up, Lo = lf.leafletLipidSeparator(value)
        nClustUp, nCoreUp, nBoundUp, nNoiseUp, silhoUp = lf.lsDBSCAN(Up,
                                                                     rCut,
                                                                     7,
                                                                     box,
                                                                     True)
        keyCoreLipids.extend(nCoreUp)
        keyClusterLipids.extend(np.add(nCoreUp, nBoundUp))

        nClustLo, nCoreLo, nBoundLo, nNoiseLo, silhoLo = lf.lsDBSCAN(Lo,
                                                                     rCut,
                                                                     7,
                                                                     box,
                                                                     True)
        keyCoreLipids.extend(nCoreLo)
        keyClusterLipids.extend(np.add(nCoreLo, nBoundLo))
        numClusters.append(nClustUp + nClustLo)

        # Worst Silhouette Coefficent of both
        silhouette_Coefficent.append(min(silhoUp, silhoLo))

        if all(core == 0 for core in keyCoreLipids):
            wMeanLipids, wSTDLipids = 0.0, 0.0
        else:
            wMeanLipids, wSTDLipids = lf.weightedMeanAndStd(keyClusterLipids,
                                                            keyCoreLipids)

        avgClusterLipids.append(wMeanLipids)
        stdClusterLipids.append(wSTDLipids)

        # Updating key Counter
        C += 1

    print("\t".join(map(str, avgClusterLipids)),
          "\t".join(map(str, stdClusterLipids)),
          "\t".join(map(str, silhouette_Coefficent)))

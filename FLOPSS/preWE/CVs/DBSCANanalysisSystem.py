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

# Sanity Check
if lipidList != rFileLipids:
    sys.exit("Lipids listed in --lipid_list and --r arguments are different.\n\
             The order in which lipids listed in both files must be same too!")

# Printing out header for output file
headerList = []
for segID in lipidList:
    headerList.append(str(segID))

header = "# " + " ".join(sys.argv)
header2 = "# System consisting of species :\t " + "\t".join(headerList)
header3 = "# Cluster-count\tCore lipid to total lipid\t\
        Cluster lipids to total lipids\t\
        Outlier lipids to total lipids\t\
        Silhouette Coefficent for lipid species"
print(header)
print(header2)
print(header3)

totalNum = len(system)

for frame in trajectory:

    box = frame.periodicBox()

    # Initializing key Counter
    C = 0
    clusterCount = 0
    coreCount = 0
    boundaryCount = 0
    outlierCount = 0
    silhouette_Coefficent = []

    # Extracting lipids to calculate centroids from the container dict
    for key, value in lipidContainer.items():

        # Collecting radius cutoff from rFile
        rCut = float(rAvgLipids[C])
        keyCoreLipids = []
        keyBoundaryLipids = []

        Up, Lo = lf.leafletLipidSeparator(value)
        nClustUp, nCoreUp, nBoundUp, nNoiseUp, silhoUp = lf.lsDBSCAN(Up,
                                                                     rCut,
                                                                     7,
                                                                     box,
                                                                     True)
        keyCoreLipids.extend(nCoreUp)
        keyBoundaryLipids.extend(nBoundUp)

        nClustLo, nCoreLo, nBoundLo, nNoiseLo, silhoLo = lf.lsDBSCAN(Lo,
                                                                     rCut,
                                                                     7,
                                                                     box,
                                                                     True)
        keyCoreLipids.extend(nCoreLo)
        keyBoundaryLipids.extend(nBoundLo)

        # Worst Silhouette Coefficent of both
        silhouette_Coefficent.append(min(silhoUp, silhoLo))

        clusterCount += (nClustUp + nClustLo)
        coreCount += np.sum(keyCoreLipids)
        boundaryCount += np.sum(keyBoundaryLipids)
        outlierCount += (nNoiseUp + nNoiseLo)

        # Updating key Counter
        C += 1

    coreLipids2Total = coreCount/totalNum
    clusterLipids2Total = (coreCount+boundaryCount)/totalNum
    outlierLipids2Total = outlierCount/totalNum

    print(clusterCount,
          coreLipids2Total,
          clusterLipids2Total,
          outlierLipids2Total,
          "\t".join(map(str, silhouette_Coefficent)))

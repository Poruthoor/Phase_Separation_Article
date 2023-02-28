#!/usr/bin/env python3
'''
Example:
    python3 segregationIndex.py --model 1DIPC.psf
                                --traj fixed_1DIPC_100.dcd
                                --lipid_list lipidList.dat
                                --r rFile.dat
'''

# Importing functional modules
import loos
import loos.pyloos
import sys
import argparse
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

# Converting model into dictionary
lipidContainer, system, lipidList = lf.segs2pyDicts(model,
                                                    args.lipidsList)

# Printing out header for output file
header = "# " + " ".join(sys.argv)
header2 = "# segregationIndex\t" + "\t".join(lipidList)
print(header)
print(header2)

for frame in trajectory:

    index = int(trajectory.realIndex())
    box = frame.periodicBox()

    # Initializing
    segregationIndex = 0
    desegregationIndex = 0
    lipidSegIndex = []
    lipidDesegIndex = []

    # Initializing key Counter
    C = 0

    Upper, Lower = lf.leafletLipidSeparator(system)

    # Extracting lipids to calculate centroids from the container dict
    for key, value in lipidContainer.items():

        # Collecting radius cutoff from rFile
        radius = float(rAvgLipids[C])

        # Separating lipids(value) to leaflets
        Up, Lo = lf.leafletLipidSeparator(value)

        # Initializing
        like = 0
        unlike = 0

        for lipid1 in Up:
            for lipid2 in Upper:
                if lipid1 != lipid2:
                    if lipid1.hardContact2D(lipid2, radius, box):
                        if lipid2[0].segid() == str(key):
                            like += 1
                        else:
                            unlike += 1

        for lipid1 in Lo:
            for lipid2 in Lower:
                if lipid1 != lipid2:
                    if lipid1.hardContact2D(lipid2, radius, box):
                        if lipid2[0].segid() == str(key):
                            like += 1
                        else:
                            unlike += 1

        total = (like+unlike)
        segIndex = like/total
        desegIndex = unlike/total

        lipidSegIndex.append(segIndex)
        lipidDesegIndex.append(desegIndex)

        segregationIndex += segIndex
        desegregationIndex += desegIndex

        # Updating key Counter
        C += 1

    print(segregationIndex, "\t", "\t".join(map(str, lipidSegIndex)))

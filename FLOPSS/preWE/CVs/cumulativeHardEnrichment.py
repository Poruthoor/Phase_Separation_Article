#!/usr/bin/env python3
'''
Example:
    python3 cumulativeHardEnrichment.py --model 1DIPC.psf
                                        --traj  fixed_1DIPC_100.dcd
                                        --lipid_list lipidList.dat
                                        --r rFile.dat
'''

# Importing functional modules
import loos
import loos.pyloos
import math
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

# Printing out header for output file
headerList = []
for segID in lipidList:
    headerList.append(str(segID)+"-"+str(segID))

header = "# " + " ".join(sys.argv)
header2 = "# cumEnrichmentAVG\t" + "\t".join(headerList)
print(header)
print(header2)


for frame in trajectory:

    box = frame.periodicBox()

    # Ideal Mixing Calcs : For Normalization of contacts
    xDim = box.x()
    yDim = box.y()
    area = (xDim*yDim)

    # Initializing
    enrichmentHardAVG = []
    cumEnrichmentAVG = 0

    # Initializing key Counter
    C = 0

    # Extracting lipids to calculate centroids from the container dict
    for key, value in lipidContainer.items():

        # Collecting radius cutoff from rFile
        radius = float(rAvgLipids[C])
        localArea = math.pi*(radius)*(radius)

        # Initializing
        avgEnrichmentHard = 0

        # Separating lipids(value) to leaflets
        Up, Lo = lf.leafletLipidSeparator(value)

        enrichmentHardUp = lf.enrichmentHard(Up, radius, area, box)
        enrichmentHardLo = lf.enrichmentHard(Lo, radius, area, box)

        avgEnrichmentHard = 0.5*(enrichmentHardUp + enrichmentHardLo)
        enrichmentHardAVG.append(avgEnrichmentHard)
        cumEnrichmentAVG += avgEnrichmentHard

        # Updating key Counter
        C += 1

    print(cumEnrichmentAVG, "\t", "\t".join(map(str, enrichmentHardAVG)))

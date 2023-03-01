import h5py
import numpy as np
import argparse

# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--directFile',
                    help='output of w_direct.py file')
parser.add_argument('--suffix',
                    default='',
                    help='File name suffix')
args = parser.parse_args()

# Read state population at every iteration

direct = h5py.File(args.directFile)
stateMatrix = np.array(direct['state_pop_evolution'])

matrixShape = np.shape(stateMatrix)
numStates = matrixShape[1]

for i in range(numStates):

    stateInfo = np.array(stateMatrix[:, i])
    # Extracting expected values
    statePop = stateInfo['expected']
    # Extracting std error values
    popSError = stateInfo['sterr']

    output = np.c_[statePop, popSError]
    stateLabel = (direct['state_labels'])[i].decode('UTF-8')
    hdr = stateLabel + " state population\tStandard Error"
    np.savetxt(args.suffix + stateLabel + "_state_population.dat",
               output,
               header=hdr,
               comments="#")

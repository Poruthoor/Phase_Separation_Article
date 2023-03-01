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
fluxMatrix = np.array(direct['target_flux_evolution'])

matrixShape = np.shape(fluxMatrix)
numStates = matrixShape[1]

for i in range(numStates):

    fluxInfo = np.array(fluxMatrix[:, i])
    # Extracting expected values
    avgFlux = fluxInfo['expected']
    # Extracting std error values
    fluxSError = fluxInfo['sterr']

    output = np.c_[avgFlux, fluxSError]
    stateLabel = (direct['state_labels'])[i].decode('UTF-8')
    hdr = "Total flux into " + stateLabel + "\tStandard Error"
    np.savetxt(args.suffix + stateLabel + "_state_total_flux.dat",
               output,
               header=hdr,
               comments="#")

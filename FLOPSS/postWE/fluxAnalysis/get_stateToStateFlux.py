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
fluxMatrix = np.array(direct['conditional_flux_evolution'])

matrixShape = np.shape(fluxMatrix)
print(matrixShape)
numStates = matrixShape[1]

for i in range(numStates):
    for j in range(numStates):
        if i != j:

            fluxInfo = np.array(fluxMatrix[:, i, j])
            # Extracting expected values
            avgFlux = fluxInfo['expected']
            # Extracting std error values
            fluxSError = fluxInfo['sterr']

            output = np.c_[avgFlux, fluxSError]

            source = (direct['state_labels'])[i].decode('UTF-8')
            sink = (direct['state_labels'])[j].decode('UTF-8')
            hdr = "Flux from " + source + " to " + sink + "\tStd Error"
            np.savetxt(args.suffix + "flux_from_" + source + "_to_" +
                       sink + ".dat",
                       output,
                       header=hdr,
                       comments="#")

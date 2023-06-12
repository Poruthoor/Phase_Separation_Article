import sys
import numpy as np
import argparse
import pyWESTPA as pw
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage


# python3 evolution.py --suffix test --temperature 323 --plotscale energy --dat_files CHE/DPPC_DAPC_CHOL/323K/1/pdist.h5 


# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--suffix',
                    help='File name suffix')
parser.add_argument('--temperature',
                    help='Temperature in Kelvin')
parser.add_argument('--plotscale',
                    help='Output option : WESTPA enehists/log10hists/blocked_hists format')
parser.add_argument('--pcoordDim',
                    help='Dimension of pcoord',
                    default=0,
                    type=int)
parser.add_argument('--dat_file',
                    help='Input file')
args = parser.parse_args()


pcoord_dim = args.pcoordDim
plotScale = args.plotscale
data = args.dat_file

kBT_factor = pw.kBT_to_kcal_per_mol(float(args.temperature))

hist, midpoints, n_iter, binbounds = pw.pdist2numpy(data, pcoord_dim)

iter_start = 1
iter_stop  = np.shape(hist)[0]

enehists, log10hists, blocked_hists, block_iters = pw.pdist2evolution(data,pcoord_dim,iter_start,iter_stop)

if plotScale == 'energy':
    plothist = kBT_factor*enehists
elif plotScale == 'log10':
    plothist = log10hists
else:
    plothist = blocked_hists

header0 = " ".join(sys.argv)
header1 = header0 + "\n# pcoord midpoint"
header2 = header0 + "\n# iternation block"
header3 = header0 + "\n# " + str(plotScale)
outputFile1 = str(args.suffix) + "_pcoordMidpoint.dat"
outputFile2 = str(args.suffix) + "_iterationBlock.dat"
outputFile3 = str(args.suffix) + "_plotHist.dat"
np.savetxt(outputFile1, midpoints, header=header1)
np.savetxt(outputFile2, block_iters, header=header2)
np.savetxt(outputFile3, plothist, header=header3)

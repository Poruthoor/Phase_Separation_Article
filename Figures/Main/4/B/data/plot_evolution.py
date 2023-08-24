import numpy as np
import argparse
import pyWESTPA as pw
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.image import NonUniformImage

# python3 plot_evolution.py --cv FLC --prefix DIPC_323K --blocked_iter test_iterationBlock.dat --midpoint test_pcoordMidpoint.dat --plotHist test_plotHist.dat --plotScale energy --xLo 0 --xUp 1 --zUp 5

# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--cv',
                    help='CV name')
parser.add_argument('--prefix',
		    help='input prefix for the plot')
parser.add_argument('--midpoint',
                    help='midpoint dat file')
parser.add_argument('--blocked_iter',
                    help='blocked_iter dat file')
parser.add_argument('--plotHist',
                    help='plothist dat file')
parser.add_argument('--plotScale',
                    help='Output option : WESTPA enehists/log10hists/blocked_hists format')
parser.add_argument('--xLo',
                    help='x axis lower limit')
parser.add_argument('--xUp',
                    help='x axis upper limit')
parser.add_argument('--zUp',
                    help='z axis upper limit')
args = parser.parse_args()

midpoints = np.loadtxt(args.midpoint)
block_iters = np.loadtxt(args.blocked_iter)
plothist = np.loadtxt(args.plotHist)

############################# Plot parameters #################################

#  plt.style.use('dark_background')

x_label = str(args.cv)
plotscale = str(args.plotScale)

norm = colors.Normalize(vmin=0, vmax=float(args.zUp))

SMALL_SIZE = 20
MEDIUM_SIZE = 20
BIGGER_SIZE = 20

plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

################################ Ploting #######################################

fig, axs = plt.subplots(sharex=True,  figsize=(8,6))

#add a big axis, hide frame
fig.add_subplot(111, frameon=False)

#hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel(str(x_label))
plt.ylabel("WE Iteration")

nui = NonUniformImage(axs, extent=(midpoints[0], midpoints[-1], block_iters[0,-1], block_iters[-1,-1]),
				  origin='lower', cmap='plasma', norm=norm)

nui.set_data(midpoints, block_iters[:,-1], plothist)


axs.add_image(nui)
axs.set_xlim(float(args.xLo), float(args.xUp))
axs.set_ylim(block_iters[0,-1], block_iters[-1,-1])

#fig.subplots_adjust(left=0.05)
cbar_ax = fig.add_axes([0.92,0.1,0.01,0.8])
cb = plt.colorbar(nui,cax=cbar_ax)

if plotscale == 'energy':
    label = r'$\Delta G(x) (kcal/mol)$' +'\n' + r'$\left[-kT \ln\,P(x)\right]$'
elif plotscale == 'log10':
    label = r'$\log_{10}\ P(x)$'
else:
    label = r'$P(x)$'

cb.set_label(label)

plt.gcf().subplots_adjust(bottom=0.15)

plt.savefig("Evolution_" + args.prefix + "_" + args.cv + ".pdf")

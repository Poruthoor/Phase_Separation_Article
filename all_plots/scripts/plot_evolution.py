import sys
import numpy as np
import argparse
import re
import pyWESTPA as pw
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.image import NonUniformImage

############################# Data Input ######################################

# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--cv',
                    help='CV name')
parser.add_argument('--suffix',
                    help='File name suffix')
parser.add_argument('--temp',
                    help='Temperature in Kelvin')
parser.add_argument('--pcoordDim',
                    help='Dimension of pcoord',
                    default=0,
                    type=int)
parser.add_argument('--fixedX',
                    default=True,
                    help='X axis is fixed')
parser.add_argument('--xLabel',
                    default="Fraction of Lipids in Clusters (FLC)",
                    help='X axis label')
parser.add_argument('--dat_files',
                    help='List of input files', nargs='+')
args = parser.parse_args()

###############################################################################

# Adapted from Stack Overflow thread : https://stackoverflow.com/a/2669120
# Alphanumeric sorting
def sorted_nicely( l ):
        """ Sort the given iterable in the way that humans expect."""
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(l, key = alphanum_key)

sorted_dat_files = (sorted_nicely(args.dat_files))

print (sorted_dat_files)

############################# Plot parameters #################################

#  plt.rcParams.update({'font.size': 14})
#  plt.style.use('dark_background')

plotscale = 'energy'
pcoord_dim = args.pcoordDim
Num_Replica = 4

norm = colors.Normalize(vmin=0, vmax=5)

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

################################ Ploting #######################################

fig, axs = plt.subplots(nrows=1, ncols=Num_Replica, sharex=True,  figsize=(18, 9))

#add a big axis, hide frame
fig.add_subplot(111, frameon=False)

#hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel(str(args.xLabel), labelpad=20)
plt.ylabel("WE Iteration", labelpad=20)

kBT_factor = pw.kBT_to_kcal_per_mol(float(args.temp))

for i in range(Num_Replica):

    print ("{0} Replica 0{1}".format(args.suffix, (i+1)))

    Replica = str(args.temp) + "K/0" +  str(i+1) + "/"

    for j in range(len(sorted_dat_files)):

        if Replica in sorted_dat_files[j]:

            print ("Processing {0}".format(sorted_dat_files[j]))

            #  iter_start, iter_stop = h5io.get_iter_range(self.input_h5['histograms']) 
            hist, midpoints, n_iter, binbounds = pw.pdist2numpy(sorted_dat_files[j], pcoord_dim)

            iter_start = 1
            iter_stop  = np.shape(hist)[0]

            enehists, log10hists, blocked_hists, block_iters = pw.pdist2evolution(sorted_dat_files[j],pcoord_dim,iter_start,iter_stop)

            if plotscale == 'energy':
                plothist = kBT_factor*enehists
            elif plotscale == 'log10':
                plothist = log10hists
            else:
                plothist = blocked_hists

            nui = NonUniformImage(axs[i], extent=(midpoints[0], midpoints[-1], block_iters[0,-1], block_iters[-1,-1]),
                                                  origin='lower', cmap='plasma', norm=norm)

            nui.set_data(midpoints, block_iters[:,-1], plothist)

            axs[i].images.append(nui)
            axs[i].set_title(str(args.temp) + ' K - Replica ' + str(i+1))

            if (args.fixedX) == True :
                axs[i].set_xlim(0, 1)
            else:
                print("BOOOOOOOOOOOOOOOOOOOOOOO")
                print(axs[i].get_xlim())

            axs[i].set_ylim(0, block_iters[-1,-1])


#  fig.subplots_adjust(left=0.05)
cbar_ax = fig.add_axes([0.92,0.1,0.01,0.8])
cb = plt.colorbar(nui,cax=cbar_ax)

if plotscale == 'energy':
    label = r'$\Delta G(x) (kcal/mol)$' +'\n' + r'$\left[-kT \ln\,P(x)\right]$'
elif plotscale == 'log10':
    label = r'$\log_{10}\ P(x)$'
else:
    label = r'$P(x)$'

cb.set_label(label)

#  plt.gcf().subplots_adjust(bottom=0.15)

plt.savefig("Evolution_" + args.suffix + "_" + args.temp + "_" + args.cv + ".png")

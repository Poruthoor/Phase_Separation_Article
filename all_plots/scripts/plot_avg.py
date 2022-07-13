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
parser.add_argument('--stride',
                    help='Step through this number of iteration intervals in each replica')
parser.add_argument('--dat_files',
                    help='List of input files', nargs='+')
args = parser.parse_args()

################################################################################

# Adapted from Stack Overflow thread : https://stackoverflow.com/a/2669120
# Alphanumeric sorting
def sorted_nicely( l ):
        """ Sort the given iterable in the way that humans expect."""
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(l, key = alphanum_key)

sorted_dat_files = (sorted_nicely(args.dat_files))

print (sorted_dat_files)

legend = set()
keyword = 'average_'

for m in range(len(sorted_dat_files)):

    group_2 = re.match("(.*?).dat", sorted_dat_files[m]).group(1)
    before2, key2, after2 = group_2.partition(keyword)

    legend.add(after2)

legend_list = sorted_nicely(list(legend))
strided_legend = legend_list[::(-1*int(args.stride))]

print ("Iterations used are ", strided_legend)

#  ############################# Plot parameters #################################

#  plt.rcParams.update({'font.size': 14})
#  plt.style.use('dark_background')

plotscale = 'energy'
xlabel = 'Fraction of Lipids in Cluster (FLC)'
Num_Replica = 4

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

#  ################################ Ploting #######################################

fig, axs = plt.subplots(nrows=1, ncols=Num_Replica, sharex=True, sharey=True, figsize=(20,8))

#add a big axis, hide frame
fig.add_subplot(111, frameon=False)

#hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)

kBT_factor = pw.kBT_to_kcal_per_mol(float(args.temp))

for i in range(Num_Replica):

    counter = 0
    for l in range(len(strided_legend)):

        FileName = str(args.temp) + "K/0" + str(i+1) + "/" + args.cv + "_average_" + str(strided_legend[l])

        for j in range(len(sorted_dat_files)):

            if FileName in sorted_dat_files[j]:

                print ("Processing {0}".format(sorted_dat_files[j]))

                Data = np.loadtxt(sorted_dat_files[j],dtype=float, comments="#")
                midpoints = Data[:,0]
                hist = Data[:,1]
                enehists = Data[:,2]
                log10hists = Data[:,3]

                if plotscale == 'energy':
                    plothist = kBT_factor*enehists
                elif plotscale == 'log10':
                    plothist = log10hists
                else:
                    plothist = blocked_hists

                axs[i].plot(midpoints,plothist,label=str(strided_legend[l]))
                axs[i].set_title(str(args.temp) + ' K - Replica ' + str(i+1))
                #  axs[h].set_xlim(midpoints[0], midpoints[-1])
                axs[i].set_xlim(0, 1)
                axs[i].set_ylim(0, 5)
                axs[i].legend(loc="upper right")

                counter += 1

        if counter == 5:
            break

if plotscale == 'energy':
    ylabel = r'$\Delta G(x) (kcal/mol)$' +'\n' + r'$\left[-kT \ln\,P(x)\right]$'
elif plotscale == 'log10':
    ylabel = r'$\log_{10}\ P(x)$'
else:
    ylabel = r'$P(x)$'

plt.ylabel(ylabel)
plt.xlabel(xlabel,labelpad=20)

plt.savefig("Convergence_" + args.suffix + "_" + args.temp + "_" + args.cv + ".png")

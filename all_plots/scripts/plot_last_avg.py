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

legend = set()
keyword = 'average_'

for m in range(len(sorted_dat_files)):

    group_2 = re.match("(.*?).dat", sorted_dat_files[m]).group(1)
    before2, key2, after2 = group_2.partition(keyword)

    legend.add(after2)

legend_list = sorted_nicely(list(legend))

print ("Iterations used are ",legend_list)

#  ############################# Plot parameters #################################

#  plt.rcParams.update({'font.size': 14})
#  plt.style.use('dark_background')

plotscale = 'energy'
Num_Replica = 4

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)   # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

#  ################################ Ploting #######################################

fig, axs = plt.subplots(figsize=(10, 6))

for h in range(Num_Replica):

    kBT_factor = pw.kBT_to_kcal_per_mol(float(args.temp))

    for l in range(len(legend)-1,0,-1):

        #  print (h, l)
        Last = False

        FileName = str(args.temp) + "K/0" + str(h+1) + "/" + args.cv + "_average_" + str(legend_list[l])

        for j in range(len(sorted_dat_files)):

            if FileName in sorted_dat_files[j]:

                print (sorted_dat_files[j])
                Last = True
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
                    plothist = hist

                #  axs[h].plot(midpoints,plothist,label=str(legend_list[l]), linewidth=2)
                #  axs[h].set_title(str(args.temp) + ' K - Replica ' + str(h+1))
                #  axs[h].set_xlim(0.0, 1.0)
                #  axs[h].set_ylim(0, 5)
                #  axs[h].legend(loc="upper right")

                axs.plot(midpoints,plothist,label=str(legend_list[l]) + ' : Replica ' + str(h+1), linewidth=2)
                axs.set_title(str(args.temp) + ' K')
                if args.fixedX:
                    axs.set_xlim(0.0, 1.0)
                axs.set_ylim(0, 5)
                axs.legend(loc="upper right")

        if Last :
            break

if plotscale == 'energy':
    ylabel = r'$\Delta G(x) (kcal/mol)$' +'\n' + r'$\left[-kT \ln\,P(x)\right]$'
elif plotscale == 'log10':
    ylabel = r'$\log_{10}\ P(x)$'
else:
    ylabel = r'$P(x)$'

plt.xlabel(str(args.xLabel))
plt.ylabel(ylabel,labelpad=20)

plt.savefig("Average_" + args.suffix + "_" + args.temp + "_" + args.cv + ".png")

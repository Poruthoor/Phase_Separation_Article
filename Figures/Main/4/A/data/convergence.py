import numpy as np
import re
import argparse
from scipy import constants
import matplotlib.pyplot as plt

# python3 convergence.py --cv FLC --suffix FLC_323K --plotScale energy --xLo 0 --xUp 1 --yUp 5 --dat_files *.dat

############################# Data Input ######################################

# Parse command-line
parser = argparse.ArgumentParser()
#  parser.add_argument('prefix', help='input prefix for the plot')
parser.add_argument('--cv',
		    help='CV name')
parser.add_argument('--temperature',
		    help='temperature')
parser.add_argument('--suffix',
		    help='File name suffix')
parser.add_argument('--plotScale',
                    help='Output option : WESTPA enehists/log10hists/blocked_hists format')
parser.add_argument('--xLo',
                    help='x axis lower limit')
parser.add_argument('--xUp',
                    help='x axis upper limit')
parser.add_argument('--yUp',
                    help='y axis upper limit')
parser.add_argument('--dat_files',
                    help='List of input files', nargs='+')
args = parser.parse_args()

def kBT_to_kcal_per_mol(Temperature):

    '''
    Output kBT value in corresponding kcal/mol units for given temperaturein Kelvin.
    '''

    kB  = constants.value('Boltzmann constant')
    Na  = constants.value('Avogadro constant')
    T   = Temperature
    E_Jules = kB*T
    E_Kcal  = E_Jules/(1000*(constants.calorie))
    E_Kcal_per_mol  = E_Kcal*Na
    return (E_Kcal_per_mol)

# Adapted from Stack Overflow thread : https://stackoverflow.com/a/2669120
# Alphanumeric sorting
def sorted_nicely( l ):
        """ Sort the given iterable in the way that humans expect."""
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(l, key = alphanum_key)

sorted_dat_files = (sorted_nicely(args.dat_files))

legend = set()
keyword = 'average_'

for m in range(len(sorted_dat_files)):

    group_2 = re.match("(.*?).dat", sorted_dat_files[m]).group(1)
    before2, key2, after2 = group_2.partition(keyword)

    legend.add(after2)

legend_list = sorted_nicely(list(legend))
kBT_factor = kBT_to_kcal_per_mol(float(args.temperature))

#  ############################# Plot parameters #################################

#  plt.style.use('dark_background')

x_label = str(args.cv)
plotscale = args.plotScale

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
#  ################################ Ploting #######################################

fig, axs = plt.subplots(sharex=True, sharey=True, figsize=(8,6))

#add a big axis, hide frame
fig.add_subplot(111, frameon=False)

#hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel(str(x_label))

for l in range(len(legend)):

	for j in range(len(sorted_dat_files)):

		if str(legend_list[l]) in sorted_dat_files[j]:
		

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

			axs.plot(midpoints,plothist,label=str(legend_list[l]))

axs.set_xlim(float(args.xLo), float(args.xUp))
axs.set_ylim(0, float(args.yUp))
axs.legend(loc="upper right")

plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig("Convergence_" + args.suffix + "_" + args.cv + ".pdf")

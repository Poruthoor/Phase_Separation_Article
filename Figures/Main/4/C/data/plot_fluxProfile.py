import numpy as np
import argparse
import matplotlib.pyplot as plt

'''
Usage :
    python3 plot_fluxProfile.py --suffix foo --dat_files *flux*.dat

'''


#  ############################# Data Input ###################################

# Parse command-line

parser = argparse.ArgumentParser()
parser.add_argument('--suffix',
                    help='suffix for filename')
parser.add_argument('--dat_files',
                    help='List of input files', nargs='+')
args = parser.parse_args()

# Taking input data files

legend = set()
keyword = '.dat'

for m in range(len(args.dat_files)):

    before1, key1, after1 = str(args.dat_files[m]).partition(keyword)

    legend.add(before1)

#  ############################# Plot parameters ##############################

#  plt.style.use('dark_background')

x_label = 'Iteration Intervals'
y_label = 'Flux ' + r'$\tau^{-1}$'

SMALL_SIZE = 20
MEDIUM_SIZE = 20
BIGGER_SIZE = 20

plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)   # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

#  ################################ Ploting ###################################

fig, axs = plt.subplots(sharex=True,
                        sharey=True,
                        figsize=(8, 6))

# add a big axis, hide frame
fig.add_subplot(111, frameon=False)

# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none',
                top=False,
                bottom=False,
                left=False,
                right=False)

plt.xlabel(x_label)
# plt.ylabel(y_label)

for j in range(len(args.dat_files)):

	legend = str(args.dat_files[j]).split(keyword)[0]
	legend = legend.replace('_', ' ')

	Data = np.loadtxt(args.dat_files[j],
			  dtype=float,
			  comments="#")

	avgPop = Data[:, 0]
	stdPop = Data[:, 1]
	iterInterval = range(np.shape(avgPop)[0])

	axs.errorbar(iterInterval,
		     avgPop,
		     yerr=stdPop,
		     fmt='-o',# alpha=0.5,
		     label=legend)

axs.set_ylim(0, 0.01)
axs.legend(loc="upper right")


plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig("flux_profile" + str(args.suffix) + ".pdf")

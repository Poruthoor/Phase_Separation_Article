import numpy as np
import argparse
import matplotlib.pyplot as plt

# python3 plot_statePop.py --suffix DIPC_323K  -dat_files *_state_population.dat

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
keyword = '_state_population.dat'

for m in range(len(args.dat_files)):

    before0, key0, after0 = str(args.dat_files[m]).partition("_avg/")
    before1, key1, after1 = str(after0).partition(keyword)

    legend.add(before1)

#  ############################# Plot parameters ##############################

#  plt.style.use('dark_background')

x_label = 'Iteration Intervals'
ylabel = 'State population'

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

fig, axs = plt.subplots(sharex=True, sharey=True, figsize=(8, 6))

# add a big axis, hide frame
fig.add_subplot(111, frameon=False)

# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', 
                top=False,
                bottom=False,
                left=False,
                right=False)

plt.xlabel(str(x_label))
plt.ylabel(ylabel)

for j in range(len(args.dat_files)):

	legend = str(args.dat_files[j]).split(keyword)[0]

	Data = np.loadtxt(args.dat_files[j],
			  dtype=float,
			  comments="#")

	avgPop = Data[:, 0]
	stdPop = Data[:, 1]
	iterInterval = range(np.shape(avgPop)[0])

	axs.errorbar(iterInterval,
		     avgPop,
		     yerr=stdPop,
		     fmt='-o',
		     label=legend)


axs.set_ylim(0, 1)
axs.legend(loc="upper right")


plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig("state_population" + str(args.suffix) + ".pdf")

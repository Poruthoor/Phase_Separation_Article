import numpy as np
import argparse
import matplotlib.pyplot as plt

#  ############################# Data Input ###################################

# Parse command-line

parser = argparse.ArgumentParser()
parser.add_argument('--suffix',
                    help='suffix for filename')
parser.add_argument('--temp',
                    help='Temperature in Kelvin')
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

print("State labels are ", legend)

#  ############################# Plot parameters ##############################

#  plt.rcParams.update({'font.size': 14})
#  plt.style.use('dark_background')

xlabel = 'Iteration Intervals'
ylabel = 'State population'

Num_Replica = 4

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)   # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

#  ################################ Ploting ###################################


fig, axs = plt.subplots(ncols=Num_Replica,
                        sharex=True,
                        sharey=True,
                        figsize=(18, 9))

# add a big axis, hide frame
fig.add_subplot(111, frameon=False)

# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none',
                top=False,
                bottom=False,
                left=False,
                right=False)

plt.xlabel(xlabel)
plt.ylabel(ylabel)

for i in range(Num_Replica):

    FileName = str(args.temp) + "K/" + str(i+1) + "/Analysis/interval_avg/"

    for j in range(len(args.dat_files)):

        if FileName in args.dat_files[j]:

            print(args.dat_files[j])

            legend = str(args.dat_files[j]).split(FileName)[-1]
            legend = legend.split(keyword)[0]

            Data = np.loadtxt(args.dat_files[j],
                              dtype=float,
                              comments="#")

            avgPop = Data[:, 0]
            stdPop = Data[:, 1]
            iterInterval = range(np.shape(avgPop)[0])

            axs[i].errorbar(iterInterval,
                            avgPop,
                            yerr=stdPop,
                            fmt='-o',
                            label=legend)

            axs[i].set_title(str(args.temp) + ' K - Replica ' + str(i+1))
            axs[i].set_ylim(0, 1)
            axs[i].legend(loc="upper right")


plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig("state_pop_" + args.suffix + "_" + args.temp + ".png")

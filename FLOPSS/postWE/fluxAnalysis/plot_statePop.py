import numpy as np
import argparse
import matplotlib.pyplot as plt

#  ############################# Data Input ###################################

# Parse command-line

parser = argparse.ArgumentParser()
parser.add_argument('--suffix',
                    help='suffix for filename')
parser.add_argument('--temp_file',
                    help='File consisting of list of temperatures')
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

x_label = 'Iteration Intervals'
ylabel = 'State population'

Num_Replica = 1

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

Temp_list = []
with open(args.temp_file) as f:
    for line in f:
        Temp_list.append(int(line))

Num_Temp = len(Temp_list)
print("Temperature  = ",Temp_list)

fig, axs = plt.subplots(ncols=Num_Temp,
                        sharex=True,
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

#  plt.xlabel(str(x_label))

for h in range(Num_Temp):

    for i in range(Num_Replica):

        FileName = str(Temp_list[h]) + "K/" + str(Num_Replica) + "/Analysis/interval_avg/"

        for j in range(len(args.dat_files)):

            if FileName in args.dat_files[j]:

                print(args.dat_files[j])

                legend = str(args.dat_files[j]).split(FileName)[-1]
                print(legend)
                legend = legend.split(keyword)[0]
                print(legend)

                Data = np.loadtxt(args.dat_files[j],
                                  dtype=float,
                                  comments="#")

                avgPop = Data[:, 0]
                stdPop = Data[:, 1]
                iterInterval = range(np.shape(avgPop)[0])

                if Num_Replica > 1:
                    if Num_Temp > 1:
                        axs[i, h].errorbar(iterInterval,
                                           avgPop,
                                           yerr=stdPop,
                                           fmt='-o',
                                           label=legend)
                    else:
                        axs[i].errorbar(iterInterval,
                                        avgPop,
                                        yerr=stdPop,
                                        fmt='-o',
                                        label=legend)

                else:
                    if Num_Temp > 1:
                        axs[h].errorbar(iterInterval,
                                        avgPop,
                                        yerr=stdPop,
                                        fmt='-o',
                                        label=legend)
                    else:
                        axs.errorbar(iterInterval,
                                     avgPop,
                                     yerr=stdPop,
                                     fmt='-o',
                                     label=legend)

                #  #  break

    if Num_Replica > 1 :

        if Num_Temp > 1:
            #  axs[i,h].set_title(str(Temp_list[h]) + ' K')

#################################################################
            #  axs[i,h].set_xlim(0.0, 1.0)
            axs[i,h].set_ylim(0, 1)
#################################################################
            axs[i,h].legend(loc="upper right")

        else:
            #  axs[i].set_title(str(Temp_list[h]) + ' K')
            #  axs[h].set_xlim(midpoints[0], midpoints[-1])
#################################################################
            #  axs[i].set_xlim(0.0, 1.0)
            axs[i].set_ylim(0, 1)
#################################################################
            axs[i].legend(loc="upper right")

    else:

        if Num_Temp > 1:

            #  axs[h].set_title(str(Temp_list[h]) + ' K')
            #  axs[h].set_xlim(midpoints[0], midpoints[-1])

#################################################################
            #  axs[h].set_xlim(0.0, 1.0)
            axs[h].set_ylim(0, 1)
#################################################################
            axs[h].legend(loc="upper right")

        else:

            #  axs.set_title(str(Temp_list[h]) + ' K')
            #  axs[h].set_xlim(midpoints[0], midpoints[-1])

#################################################################
            #  axs.set_xlim(0.0, 1.0)
            axs.set_ylim(0, 1)
#################################################################
            axs.legend(loc="upper right")

#  plt.ylabel(ylabel)

plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig("state_population" + str(args.suffix) + ".pdf")

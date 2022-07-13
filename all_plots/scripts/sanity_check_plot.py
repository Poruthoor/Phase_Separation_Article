import numpy as np
import argparse
import pyWESTPA as pw
import matplotlib.pyplot as plt

#  ############################# Data Input ###################################

# Parse command-line

parser = argparse.ArgumentParser()
parser.add_argument('--suffix',
                    help='suffix for filename')
parser.add_argument('--temp',
                    help='Temperature in Kelvin')
parser.add_argument('--vanilla_col',
                    type=int,
                    help='column number for data in vanilla file')
parser.add_argument('--dat_files',
                    help='List of input files', nargs='+')
args = parser.parse_args()

#  ############################# Plot parameters ##############################

#  plt.rcParams.update({'font.size': 14})
#  plt.style.use('dark_background')

x_label = 'Fraction of Lipids in Cluster (FLC)'
ylabel = r'$\Delta G(x) (kcal/mol)$' + '\n' + r'$\left[-kT \ln\,P(x)\right]$'
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

#  ################################ Ploting ###################################

fig, axs = plt.subplots(figsize=(10, 6))

plt.xlabel(str(x_label))

kBT_factor = pw.kBT_to_kcal_per_mol(float(args.temp))

for i in range(Num_Replica):

    FileName = str(args.temp) + "K/" + str(i+1) + "/"

    for j in range(len(args.dat_files)):

        if FileName in args.dat_files[j]:

            print(args.dat_files[j])

            legend = str(args.dat_files[j]).split(FileName)[-1]
            legend = legend.split(".dat")[0]

            if "WE-ED" in args.dat_files[j]:

                Data = np.loadtxt(args.dat_files[j],
                                  dtype=float,
                                  comments="#")
                midpoints = Data[:, 0]
                enehists = Data[:, 2]

                plothist = kBT_factor*enehists

                legend = legend + "-Replica_" + str(i+1)

                axs.plot(midpoints,
                         plothist,
                         label=legend)
                #  axs[i].plot(midpoints,
                            #  plothist,
                            #  label=legend)

            else:

                Data = np.loadtxt(args.dat_files[j],
                                  dtype=float,
                                  comments="#")

                p_coord = Data[:, args.vanilla_col]
                weights = np.ones_like(p_coord) / len(p_coord)
                im0, bin_edges = np.histogram(p_coord,
                                              bins=100,
                                              weights=weights)

                # Masking zeros to avoid log 0 issue
                im0 = np.ma.array(im0)
                masked_im0 = np.ma.masked_equal(im0, 0)

                # Mapping free energy with probability
                bin_centers = 0.5*(bin_edges[1:]+bin_edges[:-1])
                freeEnergy = -1*kBT_factor*np.log(masked_im0)
                min_freeEnergy = np.min(freeEnergy)
                shifted_free_Energy = freeEnergy - min_freeEnergy

                axs.plot(bin_centers,
                            shifted_free_Energy,
                            label=legend,
                            linestyle="dotted")

axs.set_title(str(args.temp) + ' K')
#  axs.set_xlim(midpoints[0], midpoints[-1])
axs.set_xlim(0.0, 1.0)
axs.set_ylim(0.0, 5.0)
axs.legend(loc="upper left")

                #  axs[i].plot(bin_centers,
                            #  shifted_free_Energy,
                            #  label=legend,
                            #  linestyle="dotted")

#  axs[i].set_title(str(args.temp) + ' K')
#  axs[h].set_xlim(midpoints[0], midpoints[-1])
#  axs[i].set_xlim(0.0, 1.0)
#  axs[i].set_ylim(0.0, 2.0)
#  axs[i].legend(loc="upper left")

plt.ylabel(ylabel)

plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig("sanity_check_" + str(args.suffix) + "_" + str(args.temp) + ".png")

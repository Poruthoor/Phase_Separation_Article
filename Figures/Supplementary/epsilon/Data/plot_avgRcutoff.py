import sys
import numpy as np
import argparse
import re
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from ast import literal_eval


def rFileReader(rFile):
    '''
    Read input rFile with follwing format and returns three lists:
        1. List of lipids (First coulmn)
        2. List of avg. radius (Second coulmn)
        3. List of var. of radius (Third coulmn)

    Input rFile format:
        lipid1  avg1    var1
        lipid2  avg2    var2
        ....    ....    ....

    '''
    # Initializing output lists
    rlipidList = []
    radiusList = []
    rVarList = []

    with open(rFile, 'r') as file:
        for line in file:
            # Spliting columns
            split = line.split()
            # Make sure that no empty lines are parsed as empty lists
            if split:
                rlipidList.append(split[0])
                radiusList.append(split[1])
                rVarList.append(split[2])
    return(rlipidList, radiusList, rVarList)

############################# Data Input ######################################

# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--suffix',
                    help='File name suffix')
parser.add_argument('--yRange',
                    default="(0, 2)",
                    help='yRange as a tuple')
parser.add_argument('--extraOut',
                    default=None,
                    help='Print out either "min" or "max" values of r cutoff \
                    for each species across all temp into a .dat file')
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

#  print (sorted_dat_files)

Temp = set()
legend = set()

for m in range(len(sorted_dat_files)):

    before0, key0, after0 = str(sorted_dat_files[m]).partition("K/avgRcutoff.dat")
    before1, key1, after1 = str(before0).partition("PC/")
    group_1 = ''.join(filter(str.isdigit, after1)) # Extracting just the temperature magnitude from the file path

    Temp.add(group_1)

Temp_list = sorted_nicely(list(Temp))

#  print ("Temperature  = ",Temp_list)

# Evaluating yRange
try:
    tupY = literal_eval(args.yRange)
except (SyntaxError, ValueError):
    print("%s -> Invalid tuple format given" % args.yRange)

#  ############################# Plot parameters #################################

#  plt.rcParams.update({'font.size': 14})
#  plt.style.use('dark_background')

Num_Temp = len(Temp_list)

SMALL_SIZE = 20
MEDIUM_SIZE = 20
BIGGER_SIZE = 20

plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)   # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

#  ################################ Ploting #######################################

tempLipids, tempAvg, tempVar = rFileReader(sorted_dat_files[0])
Data = np.zeros((len(tempLipids), Num_Temp, 2))

for h in range(Num_Temp):

    FileName = "PC/" + str(Temp_list[h]) + "K/avgRcutoff.dat"

    for j in range(len(sorted_dat_files)):

        if FileName in sorted_dat_files[j]:

            #  print (sorted_dat_files[j])

            for i in range(len(tempLipids)):

                lipids, avg, var = rFileReader(sorted_dat_files[j])
                Data[i][h][0] = np.asarray(avg[i])
                Data[i][h][1] = np.asarray(var[i])

fig, axs = plt.subplots(figsize=(8, 6))

for i in range(len(tempLipids)):
    axs.errorbar(Temp_list, Data[i][:, 0], Data[i][:, 1], label= str(tempLipids[i]), linewidth=3, alpha=0.5)
    axs.set_title('r cutoff vs. Temperature')
    axs.set_ylim(tupY)
    axs.legend(loc="upper right")

    if args.extraOut == "max":
        print (tempLipids[i],
              np.max(Data[i][:, 0]),
              "0")
    if args.extraOut == "min":
        print (tempLipids[i],
              np.min(Data[i][:, 0]),
              "0")

plt.xlabel("Temperature")
plt.ylabel("average R cutoff")

plt.savefig("r_vs_T_" + args.suffix + ".pdf")

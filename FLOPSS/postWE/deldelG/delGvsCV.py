import sys
import numpy as np
import argparse
import re
import pyWESTPA as pw
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from ast import literal_eval
from matplotlib.image import NonUniformImage

############################# Data Input ######################################

# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--cv',
                    help='CV name')
parser.add_argument('--suffix',
                    help='File name suffix')
parser.add_argument('--cutoff',
                    default=None,
                    help='cutoff for defining states')
parser.add_argument('--xRange',
                    default="(0, 1)",
                    help='xRange for FLC sensititvity plotting - as a tuple')
parser.add_argument('--yRange',
                    default="(-15, 15)",
                    help='yRange for del del G plotting - as a tuple')
parser.add_argument('--xLabel',
                    default="FLC",
                    help='X axis label')
#  parser.add_argument('--xBins',
                    #  default="100",
                    #  help='Num of x axis bins for CV while visualizing',
                    #  type=int)
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

print ("Files being considered = ", sorted_dat_files)

Temp = set()
legend = set()
keyword = 'average_'

# Extracting the temperature and iteration details from the files given.
# Assumption : 
# The file structure is as of following:
# DPPC-XXXX-CHOL/{TEMPERATURE}K/average_{CV}_{STARITER}-{STOPITER}.dat

for m in range(len(sorted_dat_files)):

    before0, key0, after0 = str(sorted_dat_files[m]).partition("K/")
    before1, key1, after1 = str(before0).partition("CHOL/")
    group_1 = ''.join(filter(str.isdigit, after1)) # Extracting just the temperature magnitude from the file path

    group_2 = re.match("(.*?).dat", sorted_dat_files[m]).group(1)
    before2, key2, after2 = group_2.partition(keyword)

    Temp.add(group_1)
    legend.add(after2)

Temp_list = sorted_nicely(list(Temp))
legend_list = sorted_nicely(list(legend))

print ("Temperature  = ", Temp_list)
print ("Iterations used are ", legend_list)

if len(legend) == 1:
    legendRange = range(1)
else:
    legendRange = range(len(legend)-1,0,-1)

# Evaluating xRange
try:
    tupX = literal_eval(args.xRange)
except (SyntaxError, ValueError):
    print("%s -> Invalid tuple format given" % args.xRange)

# Evaluating yRange
try:
    tupY = literal_eval(args.yRange)
except (SyntaxError, ValueError):
    print("%s -> Invalid tuple format given" % args.yRange)

#  ############################# Plot parameters #################################

#  plt.rcParams.update({'font.size': 14})
#  plt.style.use('dark_background')

Num_Temp = len(Temp_list)
tempArray = np.array(Temp_list, dtype=float)

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

ylabel = r'$\Delta \Delta G(x) (kcal/mol)$'

fig, axs = plt.subplots(figsize=(8, 6))

axs.axhline(color="grey", alpha=0.5)

# BIG ASSUMPTION : All the dat files have same number of midpoints.
# This is hardwired in my pipeline using BINEXPR variable in w_pdist stage
dataTemplate = np.loadtxt(sorted_dat_files[0],dtype=float, comments="#")
midpointsTemplate = dataTemplate[:,0]
midTemplateShape= np.shape(midpointsTemplate)

if args.cutoff == None:
    dataAll =  np.zeros((Num_Temp, midTemplateShape[0]))
else:
    dataAll =  np.zeros((Num_Temp, 1))

for h in range(Num_Temp):

    kBT_factor = pw.kBT_to_kcal_per_mol(tempArray[h])

    for l in legendRange:

        Last = False

        FileName = str(Temp_list[h]) + "K/multi_west/" + args.cv + "_average_" + str(legend_list[l])

        for j in range(len(sorted_dat_files)):

            if FileName in sorted_dat_files[j]:

                Last = True
                Data = np.loadtxt(sorted_dat_files[j],dtype=float, comments="#")
                midpoints = Data[:,0]
                hist = Data[:,1]

                midShape = np.shape(midpoints)
                probRatio = np.zeros(midShape)
                normhist = hist/np.sum(hist)

                if args.cutoff == None:

                    sortedHist = np.zeros(midShape)

                    for j in range(midShape[0]):
                        for i in range(midShape[0]):
                            if (midpoints[j] <= midpoints[i]):
                                sortedHist[j] += normhist[i]

                    # Final state = Separated , Initial State = Mixed
                    for j in range(midShape[0]):
                        probRatio[j] =  sortedHist[j]/(1-sortedHist[j])

                else:

                    sortedHist = 0

                    for i in range(midShape[0]):
                        if (float(args.cutoff) <= midpoints[i]):
                            sortedHist += normhist[i]

                    # Final state = Separated , Initial State = Mixed
                    probRatio =  sortedHist/(1-sortedHist)


                loghist = -(np.log(probRatio))

                delG = kBT_factor*loghist

                maskArray = np.isfinite(delG)
                maskedG = np.ma.array(delG, mask = ~(maskArray))

                print (delG)

                dataAll[h] = delG

                # Plotting sensitivity of FLC cutoff w.r.t to del del G
                if args.cutoff == None:
                    axs.plot(midpoints, maskedG, label= str(Temp_list[h]) + ' K' , linewidth=2)
                    #  axs.set_title('All replica combined')
                    axs.set_xlim(tupX)
                    axs.set_ylim(tupY)
                    axs.legend(loc="upper left")

        if Last :
            break

# Saving sensitivity plot of FLC cutoff w.r.t to del del G
if args.cutoff == None:

    plt.xlabel(str(args.xLabel) + " cutoff for state definition")
    plt.ylabel(ylabel)
    plt.savefig("CV_delG" + args.suffix + "_" + args.cv + ".pdf")

################################################################################

fig1, axs1 = plt.subplots(figsize=(10, 9))
axs1.axhline(color="grey", alpha=0.5)

maskArray = np.isfinite(dataAll)

#####################################################################################
# Note to Alan: This is a strict condition I enforce. let me know, if you want to do
# something about this.

# ONLY plot if there are datapoints corresponding to this FLC cutoff in every
# temperature we are considering in the datfiles. Else return an empty plot
#####################################################################################

# Masking entire CV row, if there are atleast one temp with non-finite del G values.
doubleMaskArray =  np.zeros(np.shape(maskArray), dtype=bool)
doubleMaskMid =  np.zeros(np.shape(midpoints), dtype=bool)

for i in range(np.shape(dataAll)[1]):
    if np.all(maskArray[:, i]):
        doubleMaskArray[:, i] = maskArray[:, i]
        if args.cutoff == None:
            doubleMaskMid[i] = True

maskedDataAll = np.ma.array(dataAll, mask = ~(doubleMaskArray))

if args.cutoff == None:

    maskedMid = np.ma.array(midpoints, mask = ~(doubleMaskMid))

    # Deleting masked elements for smoother plotting
    noMaskMid =  np.ma.MaskedArray.compressed(maskedMid)
    noMaskDataAll =  np.zeros((Num_Temp, np.shape(noMaskMid)[0]))

    for i in range(np.shape(maskedDataAll)[0]):
        noMaskDataAll[i] =  np.ma.MaskedArray.compressed(maskedDataAll[i])

    # Some midpoints go more decimal points unnecessarily
    # like 0.69 becoming 0.6900000000000001
    # This become a menace while using plot lables
    roundMid =  np.around(noMaskMid, decimals=4)

    for i in range(np.shape(noMaskMid)[0]):
        axs1.plot(tempArray, noMaskDataAll[:, i], label= str(args.xLabel) + ' = ' + str(roundMid[i]), linewidth=2, alpha=1)
        #  axs1.set_title(r'$\Delta \Delta G(x)$' + ' vs. Temperature')
        axs1.legend(loc="upper left")

else:

    #  noMaskDataAll =  np.zeros((Num_Temp, ))
    #  for i in range(np.shape(maskedDataAll)[0]):
        #  noMaskDataAll[i] =  np.ma.MaskedArray.compressed(maskedDataAll[i])
        #  print (noMaskDataAll[i])

    axs1.plot(tempArray, maskedDataAll, '--bo', label= str(args.xLabel) + ' = ' + args.cutoff, linewidth=2, alpha=1)
    #  axs1.set_title(r'$\Delta \Delta G(x)$' + ' vs. Temperature')
    axs1.legend(loc="upper left")

axs1.set_ylim(tupY)
axs1.set_xlim((290, 430))
#  plt.xlabel("Temperature (K)")
#  plt.ylabel(ylabel)
plt.savefig("Temp_delG" + args.suffix + "_" + args.cv + ".pdf")

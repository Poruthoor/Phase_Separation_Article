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

Num_Temp = len(Temp_list)
tempArray = np.array(Temp_list, dtype=float)

# BIG ASSUMPTION : All the dat files have same number of midpoints.
# This is hardwired in my pipeline using BINEXPR variable in w_pdist stage

dataTemplate = np.loadtxt(sorted_dat_files[0],dtype=float, comments="#")
midpointsTemplate = dataTemplate[:,0]
midTemplateShape= np.shape(midpointsTemplate)

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

                dataAll[h] = delG

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

maskedDataAll = np.ma.array(dataAll, mask = ~(doubleMaskArray))
maskedDataAll = np.reshape(maskedDataAll, (np.shape(maskedDataAll)[0], ))
print (maskedDataAll)
print (tempArray)

data2plot = np.stack((tempArray, maskedDataAll), axis=-1)
print (data2plot)

# Write out results                                                                                                                                                                                                                       
header = " ".join(sys.argv)
hdr = header +  "\n Temperature del2G"
np.savetxt("Temp_delG_" + args.suffix + "_" + args.cv + "_cutoff_" + args.cutoff + '.asc', data2plot, header=hdr, comments='#')

import numpy as np
import argparse
import re
import matplotlib.pyplot as plt

# Parse command-line
parser = argparse.ArgumentParser()
parser.add_argument('--prefix',
                    dest="prefix",
                    help='input prefix for the plot')
parser.add_argument('--column',
                    dest="column",
                    type=int,
                    help='column no. to be used from data file')
parser.add_argument('--dat_files',
                    help='List of data files', nargs='+')
args = parser.parse_args()

# Adapted from Stack Overflow thread : https://stackoverflow.com/a/2669120
# Alphanumeric sorting


def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


sorted_dat_files = (sorted_nicely(args.dat_files))
sigma_dat_files = []

# Plotting

#  plt.style.use('dark_background')
plt.rc('font', size=20)
plt.rc('legend', fontsize=20)

fig = plt.subplots(figsize=(8,6))

columnNo = args.column

for i in range(len(sorted_dat_files)):

    # Find steps and create a array to store the data
    afile = np.loadtxt(sorted_dat_files[i])
    rows = afile.shape[0]
    frames = [float(x)*0.1 for x in range(rows)]
    data = afile[:, columnNo]

    # Ignoring first data point
    #  frames = afile[1:,0]

    group_1 = re.match("(.*?)K", sorted_dat_files[i]).group(1)

    # Extracting just the temperature magnitude from the file path
    group_1 = ''.join(filter(str.isdigit, group_1))

    plt.plot(frames, data, label=('T = ' + str(group_1)))


#  plt.xlabel("Segregation Index")
#  plt.xlabel(r'Time ($\mu$s)')
plt.legend(loc="lower right")
plt.xlim(left=0,right=8)
plt.ylim(bottom=0.8, top=2.0)
#  plt.title(str(args.prefix) + " System")
plt.savefig(args.prefix + "_SegIndex.pdf")

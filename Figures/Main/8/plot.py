
#
# Usage
# python3 plot.py DATAFILE OUTPUT-SUFFIX

import matplotlib.pyplot as plt
import numpy as np
import sys

#  ############################# Plot parameters #################################

#  plt.style.use('dark_background')

FONT_SIZE = 20

plt.rc('font', size=FONT_SIZE)         # controls default text sizes
plt.rc('xtick', labelsize=FONT_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=FONT_SIZE)    # fontsize of the tick labels

#  ################################ Ploting #######################################

# Load data from a file
data = np.loadtxt(sys.argv[1])  # Replace 'your_data_file.txt' with your actual data file name

# Extract columns
column1 = data[:, 0]
column3 = data[:, 2]

# Create a plot
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.plot(column1, column3, marker='o', linestyle='-', color='b')

# Add legend
plt.ylim((-1.0, 3.0))

# Display the plot
plt.savefig(str(sys.argv[2]) + ".pdf")
# plt.savefig(str(sys.argv[2]) + ".png")
#!/usr/bin/env python
import numpy
import os
import h5py
import argparse

parser = argparse.ArgumentParser()

##Parse the input from the command line
parser.add_argument("--WEh5",
                    dest="westh5",
                    help="Path to the WE h5 file")
parser.add_argument("--first",
                    dest="first",
                    help ="Starting iteration",
                    type=int)
parser.add_argument("--last",
                    dest="last",
                    help ="Ending iteration",
                    type=int)
parser.add_argument("--total",
                    dest="total",
                    help ="Total iterations written in h5 file, If you ran 500 \
                    WE iterations, this is usually 501 accounting for next iter",
                    type=int)

args = parser.parse_args()

# WESTPA parameters
############################################

# Data types for use in the HDF5 file
seg_id_dtype = numpy.int64  # Up to 9 quintillion segments per iteration; signed so that initial states can be stored negative
n_iter_dtype = numpy.uint32  # Up to 4 billion iterations
weight_dtype = numpy.float64  # about 15 digits of precision in weights
utime_dtype = numpy.float64  # ("u" for Unix time) Up to ~10^300 cpu-seconds
vstr_dtype = h5py.special_dtype(vlen=str)
h5ref_dtype = h5py.special_dtype(ref=h5py.Reference)
binhash_dtype = numpy.dtype('|S64')

summary_table_dtype = numpy.dtype(
    [
        ('n_particles', seg_id_dtype),  # Number of live trajectories in this iteration
        ('norm', weight_dtype),  # Norm of probability, to watch for errors or drift
        ('min_bin_prob', weight_dtype),  # Per-bin minimum probability
        ('max_bin_prob', weight_dtype),  # Per-bin maximum probability
        ('min_seg_prob', weight_dtype),  # Per-segment minimum probability
        ('max_seg_prob', weight_dtype),  # Per-segment maximum probability
        ('cputime', utime_dtype),  # Total CPU time for this iteration
        ('walltime', utime_dtype),  # Total wallclock time for this iteration
        ('binhash', binhash_dtype),
    ]
)


summaryBAK = {}
counter = 0

with h5py.File(args.westh5, "r") as f:

    summaryShape = f['summary'].shape

    for i in range(args.first, (args.total) + 1):

        # Summary dataset is zero indexed
        summaryBAK[i] = f['summary'][i-1]

counter = ((args.last) - (args.first)) + 1


with h5py.File(args.westh5, "a") as f:

    del f['summary']
    dset = f.create_dataset('summary', shape=(1,), dtype=summary_table_dtype, maxshape=(None,))

    for i in range(args.first-1):

        # 1 indexed
        i = i + 1

        niter = 'iter_' + str(i).zfill(8)
        iterID = str(i).zfill(6)

        iterString = 'iterations' + '/iter_' + str(i).zfill(8) +'/'

        del f[iterString]

    for i in range(args.last, args.total):

        # 1 indexed
        i = i + 1

        niter = 'iter_' + str(i).zfill(8)
        iterID = str(i).zfill(6)

        iterString = 'iterations' + '/iter_' + str(i).zfill(8) +'/'

        del f[iterString]


    for j in range(counter):

        # 1 - indexing
        m = j + 1

        oldIterStr = 'iterations' + '/iter_' + str((args.first)+j).zfill(8) +'/'
        newIterStr = 'iterations' + '/iter_' + str(m).zfill(8) +'/'

        print (oldIterStr, " to ", newIterStr)

        f.move(oldIterStr, newIterStr)

        dset[-1] = summaryBAK[((args.first)+j)]

        dset.resize(dset.shape[0] + 1, axis=0)

        # Making sure the last iteration is a termination iteration
        if j == (counter-1):
            dset[-1] = summaryBAK[(args.total)]

    f.attrs.modify('west_current_iteration', counter)

#!/usr/bin/python

import h5py, numpy, sys
import subprocess
infile = numpy.loadtxt(sys.argv[1], usecols = (0, 1))
insert_string =[]

for iteration, seg_id in infile[1:]:
    iter_key = "{0:08d}".format(int(iteration))
    seg_key = "{0:08d}".format(int(seg_id))
    string = ["traj_segs/",iter_key,"/",seg_key,"/seg.xtc"]
    string = ''.join(string)
    insert_string.append(string)
command = ['subsetter','-C','resname =~ "PC" || resname == "CHOL"','--reimage=extreme','output','bstates/model.psf']
merged = command + insert_string
print merged
subprocess.call(merged)

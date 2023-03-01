#!/usr/bin/env python
import numpy
import os
import h5py
import argparse

parser = argparse.ArgumentParser()

##Parse the input from the command line
parser.add_argument("--WEdir",
                    dest="WEdir",
                    help="Path to the WE replica folder")
parser.add_argument("--auxLabel",
                    dest="auxLabel",
                    help="Name of the auxillary coord that need to be \
                    parsed into the h5 file. It should be same as the \
                    dir name for corresponding aux folder under \
                    fakeWEfolder")
parser.add_argument("--speciesKeyword",
                    dest="species",
                    default=False,
                    help ="Input the species, if files already exist \
                    in fakeWEfolder",
                    type=str)
parser.add_argument("--aux2D",
                    dest="aux2D",
                    default=False,
                    help ="if you gave a 2D aux data",
                    type=bool)
parser.add_argument("--first",
                    dest="first",
                    help ="Starting iteration",
                    type=int)
parser.add_argument("--last",
                    dest="last",
                    help ="Ending iteration",
                    type=int)

args = parser.parse_args()

## Path details

# Model file path
model = args.WEdir + "/bstates/model.psf"

# west.h5 file path
westh5 = args.WEdir + "/fakeWEfolder/westAux.h5"

# traj dir path
traj_dir = args.WEdir + "/traj_segs"

# Iterations info
iter = []

for x in os.listdir(traj_dir):
    if (int(x) >= args.first and int(x)<=args.last):
        iter.append(x)
iter_sorted = sorted(iter, key=int)

print ("Iterations selected for analysis : \n", iter_sorted)

with h5py.File(westh5, "a") as f:

    for i in iter_sorted:

        niter = 'iter_' + str(i).zfill(8)
        iterID = str(i).zfill(6)

        pcoordString = 'iterations' + '/iter_' + str(i).zfill(8) +'/' + 'pcoord/'

        pcoordShape = f[pcoordString].shape
        segNum = pcoordShape[0]
        pcoordLen = pcoordShape[1]

        if args.aux2D:
            pcoordDim = 2
        else:
            pcoordDim = 1

        if args.species:

            auxString = 'iterations' + '/iter_' + str(i).zfill(8) +'/auxdata/' + args.auxLabel + "_" + args.species
            fileSuffix = '_' + args.species + ".dat"

        else:
            auxString = 'iterations' + '/iter_' + str(i).zfill(8) +'/auxdata/' + args.auxLabel
            fileSuffix = ".dat"

        for seg in range(segNum):

            if (int(seg) == 0) :
                dset = f.create_dataset(auxString, (0, pcoordLen, pcoordDim) ,
                                        maxshape=(None,
                                                  pcoordLen,
                                                  pcoordDim))
            segID =  str(seg).zfill(6)
            fileName = str(segID) + fileSuffix
            file = os.path.join(args.WEdir, "fakeWEfolder", args.auxLabel,
                                str(iterID), fileName)
            data = numpy.loadtxt(file, dtype=float)
            data = numpy.reshape(data, (pcoordLen, pcoordDim))
            dset.resize(dset.shape[0] + 1, axis=0)
            dset[-1,:,:] = data

#! /bin/bash

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Vanilla_files_transfer.sh                                                            #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################


# # Creating separate dir for Temp runs w.r.t Tm
for P in ClusterLipids2Total
do
    for i in DAPC DIPC POPC
    do
        for T in 298K 333K 343K 373K 323K 353K 423K 450K
        do
            for d in 1 2 3 4
            do
                if [ -e $CURRENT/$P/DPPC_${i}_CHOL/$T/0${d}/west.h5 ] ; then

                    mkdir -p $CURRENT/Sanity_Check/$P/$i/$T/$d/
                    rm -rf $CURRENT/Sanity_Check/$P/$i/$T/$d/*.dat

                    if [ -e ../CVs4PhaseSeparation/production_phase/cv_validation/analysis/data/$i/$T/$d/DBSCANanalysisSystem.dat ] ; then

                        File=../CVs4PhaseSeparation/production_phase/cv_validation/analysis/data/$i/$T/$d/DBSCANanalysisSystem.dat
                        echo "Old File = " $File
                        New_File="Standard-MD-Replica_${d}.dat"
                        echo "New file = " $New_File
                        cp $File $CURRENT/Sanity_Check/$P/$i/$T/$d/$New_File

                        cd $CURRENT
                    fi
                fi
            done
        done
    done
done

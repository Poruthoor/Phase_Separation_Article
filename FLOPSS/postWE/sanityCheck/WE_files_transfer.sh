#! /bin/bash

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash WE_files_transfer.sh                                                            #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

# Creating separate dir for Temp runs w.r.t Tm
for P in ClusterLipids2Total
do
    for i in DAPC # DIPC POPC
    do
        for T in 353K # 298K 333K 343K 373K 323K 353K 423K 450K
        do
            for d in 1 2 3 4
            do

                if [ -e $CURRENT/$P/DPPC_${i}_CHOL/$T/0${d}/west.h5 ] ; then

                    cd $CURRENT/$P/DPPC_${i}_CHOL/$T/0${d}/
                    rm -rf $CURRENT/Sanity_Check/$P/$i/$T/$d/*WE-ED_*.dat

                    File=$(ls -1tr *.dat | tail -1)
                    echo "Old File = " $File
                    New_File=$(ls -1tr *.dat | tail -1 | sed -e "s/${P}_average_/WE-ED_/")
                    echo "New file = " $New_File
                    mkdir -p $CURRENT/Sanity_Check/$P/$i/$T/$d
                    cp $File $CURRENT/Sanity_Check/$P/$i/$T/$d/$New_File

                    # for iter in 1 2 3 4 5
                    # do
                        # TAIL=$(($iter*5))
                        # File=$(ls -1tr *.dat | tail -$TAIL | head -1)
                        # echo "Old File = " $File
                        # New_File=$(ls -1tr *.dat | tail -$TAIL | head -1 | sed -e "s/${P}_average_/WE-ED_/")
                        # echo "New file = " $New_File
                        # cp $File $CURRENT/Sanity_Check/$P/$i/$T/$d/$New_File
                    # done
                    cd $CURRENT
                fi
            done
        done
    done
done

#! /bin/bash

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Analysis.sh                                                            #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

# Creating separate dir for Temp runs w.r.t Tm
for i in DAPC DIPC POPC
do
    for P in ClusterLipids2Total
    do
        for T in 298K 323K 333K 343K 353K 373K 423K 450K
        do
            for d in 1 2 3 4
            do

                if [ -e /Ashlin5/ashlin/Phase_Seperation/Weighted_Ensemble_3/$P/DPPC_${i}_CHOL/$T/$d/west.h5 ]
                then

                    cd /Ashlin5/ashlin/Phase_Seperation/Weighted_Ensemble_3/$P/DPPC_${i}_CHOL/$T/$d/

                    cp -prf $CURRENT/copy2MainWEdir/* .

                    sed -i 's/XXXX/'${i}'/g' parseAuxData.sh

                    cd $CURRENT
                fi
            done
        done
    done
done

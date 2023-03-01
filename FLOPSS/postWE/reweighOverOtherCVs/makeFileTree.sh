#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH -J makeFileTree
#SBATCH -o makeFileTree_o
#SBATCH -e makeFileTree_e

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
for i in DIPC  # DAPC DIPC POPC
do
    for P in ClusterLipids2Total
    do
        for T in 323K # 298K 323K 333K 343K 353K 373K 423K 450K
        do
            for d in 1 # 2 3 4
            do

                if [ -e ${CURRENT}/${P}/DPPC_${i}_CHOL/${T}/0${d}/west.h5 ] ; then

                    mkdir -pv ${CURRENT}/${P}_OtherCVs/DPPC_${i}_CHOL/${T}/0${d}

                    cd ${CURRENT}/${P}_OtherCVs/DPPC_${i}_CHOL/${T}/0${d}/

                    cp -prf ${CURRENT}/${P}/DPPC_${i}_CHOL/${T}/0${d}/fakeWEfolder/westAux.h5 west.h5

                    # python3 ${CURRENT}/ReweighOverOtherCVs/truncate.py --WEh5 west.h5 --first 490 --last 500 --total 501
                    python3 ${CURRENT}/ReweighOverOtherCVs/truncate.py --WEh5 west.h5 --first 250 --last 500 --total 501

                    # w_truncate -n 12
                    w_truncate -n 252

                    cd $CURRENT
                fi
            done
        done
    done
done

#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH -J pdist2data_multi_Reweigh
#SBATCH -o pdist2data_multi_Reweigh_o
#SBATCH -e pdist2data_multi_Reweigh_e

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Plot.sh                                                                #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

for i in DAPC DIPC POPC
do
    for P in ClusterLipids2Total_OtherCVs
    do
        for T in 298K 323K 333K 343K 353K 373K 423K 450K
        do
            if [ -e $CURRENT/${P}/DPPC_${i}_CHOL/${T}/multi_west/west.h5 ]; then
                cd $CURRENT/${P}/DPPC_${i}_CHOL/${T}/multi_west
                iterstart=0
                iterstop=10
                interval=10

                STOP=$(echo "$(($iterstop - $(($iterstart-1)))) / $interval" | bc)

                    for j in $(seq 0 $(($STOP-1)))
                    do
                        STARTiter=$(($iterstart+$(($j*$interval))))
                        echo $STARTiter
                        STOPiter=$(($iterstart+$(($(($j+1))*$interval))))
                        echo $STOPiter
                        echo "plothist average pdist.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${P}_average_${STARTiter}-${STOPiter}.dat"
                        plothist average pdist.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${P}_average_${STARTiter}-${STOPiter}.dat
                    done
                cd $CURRENT
            fi
        done
    done
done

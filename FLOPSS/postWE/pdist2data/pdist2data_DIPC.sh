#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH -J pdist2data_DIPC
#SBATCH -o pdist2data_DIPC_o
#SBATCH -e pdist2data_DIPC_e

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

for P in ClusterLipids2Total
do
    for T in 298K 323K 353K 423K
    do
        for d in 1 2 3 4
        do
            WORKDIR=/scratch/aporutho/LipidPhase/Simulation/Weighted_Ensemble_3/Analysis/$P/DPPC_DIPC_CHOL/$T/0${d}/
            mkdir -p $CURRENT/$P/DPPC_DIPC_CHOL/$T/0${d}/
            cd $WORKDIR/
            iterstart=1
            iterstop=500
            interval=10

            STOP=$(echo "$(($iterstop - $(($iterstart-1)))) / $interval" | bc)

                for j in $(seq 0 $(($STOP-1)))
                do
                    STARTiter=$(($iterstart+$(($j*$interval))))
                    STOPiter=$(($(($iterstart+$(($(($j+1))*$interval))))-1))
                    echo "${STARTiter} - ${STOPiter}"
                    echo "plothist average pdist.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${CURRENT}/${P}/DPPC_DIPC_CHOL/$T/0${d}/${P}_average_${STARTiter}-${STOPiter}.dat"
                    plothist average pdist.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${CURRENT}/${P}/DPPC_DIPC_CHOL/$T/0${d}/${P}_average_${STARTiter}-${STOPiter}.dat
                done
            cd $CURRENT
        done
    done
done

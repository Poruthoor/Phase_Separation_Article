#! /bin/bash
#SBATCH -p standard
#SBATCH -t 08:00:00
#SBATCH -c 1
#SBATCH -J flux_POPC
#SBATCH -o flux_POPC_o
#SBATCH -e flux_POPC_e

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
for i in POPC 
do
    for P in ClusterLipids2Total 
    do
        for T in 298K 450K
        do
            for d in 1 2 3 4
            do
                mkdir -pv $CURRENT/$P/DPPC_${i}_CHOL/$T/$d
                rsync -av /scratch/aporutho/LipidPhase/Simulation/Weighted_Ensemble_3/$P/DPPC_${i}_CHOL/$T/$d/west.h5 $CURRENT/$P/DPPC_${i}_CHOL/$T/$d

                if [ -e $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/west.h5 ] ; then

                    cd $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/

                    rm -rf west.cfg

                    cp -pf $CURRENT/WEST_CFG_TEMPLATE/cumulative/$P/west.cfg . 

                    w_ipa -ao 

                    rm -rf west.cfg

                    cp -pf $CURRENT/WEST_CFG_TEMPLATE/interval_avg/$P/west.cfg .

                    w_ipa -ao 

                    cd $CURRENT
                fi
            done
        done
    done
done

#! /bin/bash
#SBATCH -p standard
#SBATCH -t 04:00:00
#SBATCH -c 1
#SBATCH -J west2pdist
#SBATCH -o west2pdist_o
#SBATCH -e west2pdist_e

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

BINEXPR=$(echo $(python3 ${CURRENT}/binGenerator.py --binRange "(0, 1)" --Num_bins_plusOne 101))

# Creating separate dir for Temp runs w.r.t Tm
for i in DAPC DIPC POPC
do
    for P in ClusterLipids2Total # ClusterLipids2Total_Extended_NoReweighting
    do
        for T in 298K 333K 343K 373K 323K 353K 423K 450K
        do
            for d in 1 2 3 4
            do

                if [ -e /scratch/aporutho/LipidPhase/Simulation/Weighted_Ensemble_3/$P/DPPC_${i}_CHOL/$T/$d/west.h5 ] ; then

                    mkdir -pv $CURRENT/$P/DPPC_${i}_CHOL/$T/0${d}
                    rsync -av /scratch/aporutho/LipidPhase/Simulation/Weighted_Ensemble_3/$P/DPPC_${i}_CHOL/$T/$d/west.h5 $CURRENT/$P/DPPC_${i}_CHOL/$T/0${d}

                    cd $CURRENT/$P/DPPC_${i}_CHOL/$T/0${d}/

                    rm -f *.pdf *.dat
                    rm pdist.h5

                    w_pdist -b "[${BINEXPR}]" --serial

                    plothist evolution pdist.h5 -o evolution_${i}_${P}_${T}_${d}.pdf

                    cd $CURRENT
                fi
            done
        done
    done
done

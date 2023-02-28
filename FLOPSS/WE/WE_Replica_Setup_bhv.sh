#!/bin/bash
#SBATCH --partition=gpu-debug
#SBATCH --gres=gpu:1
#SBATCH --time=01:00:00
#SBATCH --mem=15G
#SBATCH --job-name=ReplicaPrep
#SBATCH --output=ReplicaPrep.out
#SBATCH --error=ReplicaPrep.err

###############################################################################
# Usage                                                                       #
#                                                                             #
# WE_Replica_Setup_bhv.sh > WE_Replica_Setup_bhv.out                          #
#                                                                             #
# Example                                                                     #
#                                                                             #
# bash WE_Replica_Setup_bhv.sh > WE_Replica_Setup_bhv.out                     #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD

###############################################################################
#             2. COPYING INITIAL REPLICATES FURTHER FOR Tm RUNS               #
###############################################################################

# Creating separate dir for Temp runs w.r.t Tm
for P in 2DMeanVsSTD CumHardEnrich ClusterLipids2Total
do
    for i in DAPC # DIPC POPC
    do
        for T in 298K 323K 333K 343K 353K 373K 423K
        do
            mkdir -pv $CURRENT/$P/DPPC_${i}_CHOL/$T
            cp -pr $CURRENT/DPPC_${i}_CHOL/1 $CURRENT/$P/DPPC_${i}_CHOL/$T/
            cp -pr $CURRENT/DPPC_${i}_CHOL/2 $CURRENT/$P/DPPC_${i}_CHOL/$T/
            cp -pr $CURRENT/DPPC_${i}_CHOL/3 $CURRENT/$P/DPPC_${i}_CHOL/$T/
            cp -pr $CURRENT/DPPC_${i}_CHOL/4 $CURRENT/$P/DPPC_${i}_CHOL/$T/

            for d in 1 2 3 4
            do
                mkdir -pv $CURRENT/$P/DPPC_${i}_CHOL/$T/$d
                cp -rf WE_Template/* $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/
                cp -rf PCOORD_Template/$P/* $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/
                cp -rf ../preWE/xy_rdf/$i/lipidList.dat $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/common_files/
                cp -rf ../preWE/xy_rdf/$i/$T/avgRcutoff.dat  $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/common_files/
                cp -rf MDP_Template/$i/$T/md.mdp   $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/common_files/
                sed -i "s/WESTPA_RUN/${P}_${i}_${T}_${d}/g" $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/run.sh
            done
        done
    done
done

for P in SegIndex
do
    for i in DAPC # DIPC POPC
    do
        for T in 298K 323K 333K 343K 353K 373K 423K
        do
            mkdir -pv $CURRENT/$P/DPPC_${i}_CHOL/$T
            cp -pr $CURRENT/DPPC_${i}_CHOL/1 $CURRENT/$P/DPPC_${i}_CHOL/$T/
            cp -pr $CURRENT/DPPC_${i}_CHOL/2 $CURRENT/$P/DPPC_${i}_CHOL/$T/
            cp -pr $CURRENT/DPPC_${i}_CHOL/3 $CURRENT/$P/DPPC_${i}_CHOL/$T/
            cp -pr $CURRENT/DPPC_${i}_CHOL/4 $CURRENT/$P/DPPC_${i}_CHOL/$T/

            for d in 1 2 3 4
            do
                mkdir -pv $CURRENT/$P/DPPC_${i}_CHOL/$T/$d
                cp -rf WE_Template/* $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/
                cp -rf PCOORD_Template/$P/* $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/
                cp -rf ../preWE/xy_rdf/$i/lipidList_NO_CHOL.dat $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/common_files/
                cp -rf ../preWE/xy_rdf/$i/$T/avgRcutoff_NO_CHOL.dat  $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/common_files/
                cp -rf MDP_Template/$i/$T/md.mdp   $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/common_files/
                sed -i "s/WESTPA_RUN/${P}_${i}_${T}_${d}/g" $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/run.sh
            done
        done
    done
done

# ###############################################################################

#! /bin/bash

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

for P in CumHardEnrich SegIndex ClusterLipids2Total
do
    for L in DIPC DAPC # POPC
    do
        for T in 323K
        do
            for R in 1 # 2 3 4
            do
                cd $CURRENT/$P/DPPC_${L}_CHOL/${T}/${R}/Analysis/interval_avg/

                python3 ../../../../../../get_statePopulation.py --directFile=direct.h5
                python3 ../../../../../../get_stateToStateFlux.py --directFile=direct.h5
                python3 ../../../../../../get_stateTargetFlux.py --directFile=direct.h5

                cd $CURRENT
            done
        done
        python3 plot_statePop.py --suffix ${P}_${L} --temp_file tempList.dat --dat_files $P/DPPC_${L}_CHOL/*K/*/Analysis/interval_avg/*state_population.dat
        # python3 plot_fluxProfile.py --suffix ${P}_${L} --temp_file tempList.dat --dat_files $P/DPPC_${L}_CHOL/*K/*/Analysis/interval_avg/*flux*.dat
        python3 plot_fluxProfile.py --suffix ${P}_${L} --temp_file tempList.dat --dat_files $P/DPPC_${L}_CHOL/*K/*/Analysis/interval_avg/flux*.dat
    done
done


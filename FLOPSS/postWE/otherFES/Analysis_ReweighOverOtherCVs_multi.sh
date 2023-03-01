#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH -J Reweigh_multi
#SBATCH -o Reweigh_multi_o
#SBATCH -e Reweigh_multi_e

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Analysis.sh                                                            #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD
STARTiter=0
STOPiter=10

AuxHeaders=("CHE"
            "CHE_CHOL"
            "CHE_DXPC"
            "CHE_DPPC"
            "SI"
            "SI_CHOL"
            "SI_DXPC"
            "SI_DPPC"
            "SI_WithoutCHOL"
            "SI_WithoutCHOL_DXPC"
            "SI_WithoutCHOL_DPPC"
            "pcoord"
            "DBSCAN_fixed_min"
            "DBSCAN_fixed_max"
            "mops_CHOL"
            "mops_DPPC"
            "mops_DIPC"
            "mops_DAPC"
            "mops_POPC"
            )

AuxHeadersOCV36=("CHE")
AuxHeadersOCV083=("CHE_DXPC")
AuxHeadersOCV082=("SI"
                "SI_WithoutCHOL"
                "CHE_CHOL"
                "CHE_DPPC"
                )
AuxHeadersOCV01=("pcoord"
                "DBSCAN_fixed_min"
                "DBSCAN_fixed_max"
                "SI_CHOL"
                "SI_DXPC"
                "SI_DPPC"
                "SI_WithoutCHOL_DXPC"
                "SI_WithoutCHOL_DPPC"
                )
AuxHeadersOCV2D=("weightedCluster_CHOL"
                "weightedCluster_DXPC"
                "weightedCluster_DPPC"
                "mops2D_CHOL"
                "mops2D_DPPC"
                "mops2D_DIPC"
                "mops2D_DAPC"
                "mops2D_POPC"
                )
AuxHeadersOCV005=("mops_CHOL"
                "mops_DPPC"
                "mops_DIPC"
                "mops_DAPC"
                "mops_POPC"
                )

AuxHeaders2D=("weightedCluster_CHOL"
            "weightedCluster_DXPC"
            "weightedCluster_DPPC"
            "mops2D_CHOL"
            "mops2D_DPPC"
            "mops2D_DIPC"
            "mops2D_DAPC"
            "mops2D_POPC"
            )

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

# BINEXPR=$(echo $(python3 ${CURRENT}/binGenerator.py --binRange "(0, 1)" --Num_bins_plusOne 101))

# Creating separate dir for Temp runs w.r.t Tm
for i in DAPC DIPC POPC
do
    for P in ClusterLipids2Total_OtherCVs
    do
        for T in 298K 323K 353K 423K 450K 333K 343K 373K 
        do
            for d in multi_west
            do

                if [ -e $CURRENT/${P}/DPPC_${i}_CHOL/$T/$d/west.h5 ] ; then

                    mkdir -pv $CURRENT/${P}_AuxData/DPPC_${i}_CHOL/$T/$d

                    rsync -av $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/west.h5 $CURRENT/${P}_AuxData/DPPC_${i}_CHOL/$T/$d

                    cd $CURRENT/${P}_AuxData/DPPC_${i}_CHOL/$T/$d/

                    cp -prf $CURRENT/ReweighOverOtherCVs/module.py .

                    rm -f *.pdf *.dat

                    for aux in "${AuxHeaders[@]}"
                    do

                        # w_pdist -b "[${BINEXPR}]" -o ${aux}.h5 --construct-dataset module.load_${aux} --serial

                        w_pdist -o ${aux}.h5 --construct-dataset module.load_${aux} --serial

                        plothist average ${aux}.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${aux}_average_${STARTiter}-${STOPiter}.dat

                    done

                    # for aux in "${AuxHeaders2D[@]}"
                    # do

                        # w_pdist  -o ${aux}.h5 --construct-dataset module.load_${aux} --serial

                        # plothist average ${aux}.h5 0 1 --first-iter $STARTiter --last-iter $STOPiter -o ${aux}_average_${STARTiter}-${STOPiter}.pdf

                    # done
              
                    cd $CURRENT
                fi
            done
        done
    done
done

#! /bin/bash
#SBATCH -p standard
#SBATCH -t 08:00:00
#SBATCH -c 1
#SBATCH -J OtherFES_multi
#SBATCH -o OtherFES_multi_o
#SBATCH -e OtherFES_multi_e

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Analysis.sh                                                            #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD
STARTiter=490
STOPiter=500

AuxHeaders00=("clucountchol"
              "clucountdppc"
              "clucountdxpc"
              "clucounttotal"
              )

AuxHeaders01=("clusbychol"
              "clusbydppc"
              "clusbydxpc"
              "corebychol"
              "corebydppc"
              "corebydxpc"
              "corebytotal"
              "outbytotal"
              )

AuxHeaders11=("silcoeffchol"
              "silcoeffdppc"
              "silcoeffdxpc"
              )

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

# BINEXPR00=$(echo $(python3 ${CURRENT}/binGenerator.py --binRange "(0, 100)" --Num_bins_plusOne 101))
# BINEXPR01=$(echo $(python3 ${CURRENT}/binGenerator.py --binRange "(0, 1)" --Num_bins_plusOne 101))
# BINEXPR11=$(echo $(python3 ${CURRENT}/binGenerator.py --binRange "(-1, 1)" --Num_bins_plusOne 101))

# Creating separate dir for Temp runs w.r.t Tm
for i in DAPC DIPC POPC
do
    for P in ClusterLipids2Total
    do
        for T in 298K 333K 343K 373K 323K 353K 423K 450K
        do
            for d in multi_west
            do

                if [ -e $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/west.h5 ] ; then

                    mkdir -pv $CURRENT/${P}_AuxData/DPPC_${i}_CHOL/$T/$d

                    rsync -av $CURRENT/$P/DPPC_${i}_CHOL/$T/$d/west.h5 $CURRENT/${P}_AuxData/DPPC_${i}_CHOL/$T/$d

                    cd $CURRENT/${P}_AuxData/DPPC_${i}_CHOL/$T/$d/

                    cp -prf $CURRENT/OtherFES/module.py .

                    rm -f *.pdf *.dat

                    for aux in "${AuxHeaders00[@]}"
                    do

                        # w_pdist  -o ${aux}.h5 --construct-dataset module.load_${aux} -b "[${BINEXPR00}]" --serial
                        w_pdist  -o ${aux}.h5 --construct-dataset module.load_${aux} --serial

                        plothist average ${aux}.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${aux}_average_${STARTiter}-${STOPiter}.dat

                    done

                    for aux in "${AuxHeaders01[@]}"
                    do

                        # w_pdist  -o ${aux}.h5 --construct-dataset module.load_${aux} -b "[${BINEXPR01}]" --serial
                        w_pdist  -o ${aux}.h5 --construct-dataset module.load_${aux} --serial

                        plothist average ${aux}.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${aux}_average_${STARTiter}-${STOPiter}.dat

                    done

                    for aux in "${AuxHeaders11[@]}"
                    do

                        # w_pdist  -o ${aux}.h5 --construct-dataset module.load_${aux} -b "[${BINEXPR11}]" --serial
                        w_pdist  -o ${aux}.h5 --construct-dataset module.load_${aux} --serial

                        plothist average ${aux}.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=${aux}_average_${STARTiter}-${STOPiter}.dat

                    done

                    cd $CURRENT
                fi
            done
        done
    done
done

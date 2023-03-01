#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH -J combine
#SBATCH -o combine_o
#SBATCH -e combine_e

###############################################################################
#                                                                             #
# Usage                                                                       #
#                                                                             #
# bash Analysis.sh                                                            #
#                                                                             #
###############################################################################

###############################################################################
#                                                                             #
#                               !! WARNING !!                                 #
#                                                                             #
# From my experience, the w_pdist in this script is highly likely to throw a  #
# fatal threading error, but the output file after this fatal error and       #
# subsequent core dump, seems to same as the output file created without any  #  
# errors (after running directly in the folder)                               #
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
    for P in ClusterLipids2Total
    do
        for T in 298K 323K 333K 343K 353K 373K 423K 450K
        do

            if [ -d $CURRENT/${P}_OtherCVs/DPPC_${i}_CHOL/$T/ ] ; then

                cd $CURRENT/${P}_OtherCVs/DPPC_${i}_CHOL/$T/

                ##################################################################################
                ##################################################################################
                # If the automated bash script throws a fatal threading error,
                # following command to be done manually inside the top dir of replica 
                ##################################################################################
                ##################################################################################

                cp -prf /scratch/aporutho/LipidPhase/Simulation/Weighted_Ensemble_3/$P/DPPC_${i}_CHOL/$T/1/adaptive.py .
                w_multi_west -m . -n 4 --auxall --debug

                ##################################################################################
                # If you are executing above 2 lines since you encountered a fatal error:
                # Once the manual execution is done,
                # Comment out the above 2 lines and rerun this script again to make necessary
                # clean up and file tree creation.
                # Then rerun commands after this
                ##################################################################################

                mkdir -p multi_west/

                mv multi.h5 multi_west/west.h5
                mv adaptive.py multi_west/
                rm -rf __pycache__

                cd multi_west/

                rm -f *.pdf *.dat
                rm pdist.h5

                ##################################################################################
                ##################################################################################
                # If the automated bash script throws a fatal threading error,
                # following command to be done manually inside the multi_west dir,
                ##################################################################################
                ##################################################################################

                w_pdist -b "[${BINEXPR}]" --serial

                plothist evolution pdist.h5 -o evolution_${i}_${P}_${T}.pdf

            fi

            cd $CURRENT

        done
    done
done

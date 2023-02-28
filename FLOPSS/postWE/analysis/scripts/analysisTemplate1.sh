#!/bin/bash
###############################################################################
#                                                                             #
# Note : This bash script considers CHOLESTEROL as well. i.e, lipidlist and   #
#        radiusCutoff files have chloesterol in it                            #
# Usage :                                                                     #
#   bash analysisTemplate1.sh analysisPythonScriptFileName                    #  
#                                                                             #
# Disclaimer : You need to install LOOS in your env                           # 
###############################################################################

CURRENT=$PWD
WORKDIR=$CURRENT/../../../CVs4PhaseSeparation
PYTHON_PREFIX=$1

for SYSTEM in DAPC DIPC POPC
do
    rm -rf ${WORKDIR}/analysis/data/${SYSTEM}/*/*/${PYTHON_PREFIX}.*
    list=${WORKDIR}/xy_rdf/${SYSTEM}/lipidList.dat

    for i in 298K 323K 423K 450K
    do
        rFile=${WORKDIR}/xy_rdf/${SYSTEM}/${i}/avgRcutoff.dat

       for j in 1 2 3 4 
       do

            traj=/Ashlin2/ashlin/Phase_Seperation/Analysis/Trajectory/${SYSTEM}/${j}/${i}/fixed_${j}${SYSTEM}_100.dcd
            model=/Ashlin2/ashlin/Phase_Seperation/Analysis/Trajectory/${SYSTEM}/${j}/${i}/${j}${SYSTEM}.psf

            if [ -s $traj ] && [ -s $model ]
            then

                mkdir -p ${WORKDIR}/analysis/data/${SYSTEM}/${i}/${j}
                cd ${WORKDIR}/analysis/data/${SYSTEM}/${i}/${j}/


                echo "Calculating ${PYTHON_PREFIX} for ${SYSTEM} : Replica ${j} at Temperature ${i}"

                python3 ${WORKDIR}/CVs/${PYTHON_PREFIX}.py --model ${model} \
                    --traj ${traj} \
                    --lipid_list ${list} \
                    --r ${rFile} >> ${PYTHON_PREFIX}.dat
            fi

            cd ${WORKDIR}
        done
    done
done

#!/bin/bash

WORKDIR=../../../analysis
SCRIPTDIR=../../scripts
SYSTEM=POPC
SUFFIX=_NO_CHOL

for i in 1 # 2 3 4
do
    prefix=weighted_${i}${SYSTEM}${SUFFIX}

    counter=0

    for segid in DPPC ${SYSTEM}
    do


        python3 ${SCRIPTDIR}/plot_DBSCANspeciesMeanLipidsPerClust.py --prefix ${prefix} --segid ${segid} --column $((0+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/wDBSCANanalysisSpecies${SUFFIX}.dat

        python3 ${SCRIPTDIR}/plot_DBSCANspeciesSTDLipidsPerClust.py --prefix ${prefix} --segid ${segid} --column $((2+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/wDBSCANanalysisSpecies${SUFFIX}.dat

        counter=$((counter+1))
    done
done


#!/bin/bash

WORKDIR=../../../analysis
SCRIPTDIR=../../scripts
SYSTEM=DAPC

for i in 1 2 3 4
do
    prefix=weighted_${i}${SYSTEM}

    counter=0

    for segid in DPPC ${SYSTEM} CHOL
    do


        python3 ${SCRIPTDIR}/plot_DBSCANspeciesMeanLipidsPerClust.py --prefix ${prefix} --segid ${segid} --column $((0+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/wDBSCANanalysisSpecies.dat

        python3 ${SCRIPTDIR}/plot_DBSCANspeciesSTDLipidsPerClust.py --prefix ${prefix} --segid ${segid} --column $((3+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/wDBSCANanalysisSpecies.dat

        counter=$((counter+1))
    done
done

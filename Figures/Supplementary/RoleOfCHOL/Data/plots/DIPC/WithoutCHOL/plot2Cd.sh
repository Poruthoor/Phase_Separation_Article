#!/bin/bash

WORKDIR=../../../analysis
SCRIPTDIR=../../scripts
SYSTEM=DIPC
SUFFIX=_NO_CHOL

for i in 1 2 3 4
do
    prefix=${i}${SYSTEM}${SUFFIX}

    counter=0

    for segid in DPPC ${SYSTEM}
    do


        python3 ${SCRIPTDIR}/plot_DBSCANspeciesMeanLipidsPerClust.py --prefix ${prefix} --segid ${segid} --column $((12+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/DBSCANanalysisSpecies${SUFFIX}.dat

        python3 ${SCRIPTDIR}/plot_DBSCANspeciesSTDLipidsPerClust.py --prefix ${prefix} --segid ${segid} --column $((14+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/DBSCANanalysisSpecies${SUFFIX}.dat

        counter=$((counter+1))
    done
done


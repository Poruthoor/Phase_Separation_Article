#!/bin/bash

WORKDIR=../../../analysis
SCRIPTDIR=../../scripts
SYSTEM=DIPC

for i in 1 2 3 4
do
    prefix=${i}${SYSTEM}

    counter=0

    for segid in DPPC ${SYSTEM} CHOL
    do


        python3 ${SCRIPTDIR}/plot_DBSCANspeciesMeanCorePerClust.py --prefix ${prefix} --segid ${segid} --column $((12+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/DBSCANanalysisSpecies.dat

        python3 ${SCRIPTDIR}/plot_DBSCANspeciesSTDCorePerClust.py --prefix ${prefix} --segid ${segid} --column $((15+counter)) --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/DBSCANanalysisSpecies.dat

        counter=$((counter+1))
    done
done


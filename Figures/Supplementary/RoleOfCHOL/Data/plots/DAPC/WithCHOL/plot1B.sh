#!/bin/bash

WORKDIR=../../../analysis
SCRIPTDIR=../../scripts
SYSTEM=DAPC

for i in 1 2 3 4
do
    prefix=${i}${SYSTEM}

    counter=1

    for segid in DPPC ${SYSTEM} CHOL
    do


        # python3 ${SCRIPTDIR}/plot_CHEcomponents.py --prefix ${prefix} --segid ${segid} --column ${counter} --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/cumulativeHardEnrichment.dat

        python3 ${SCRIPTDIR}/plot_SegIndexComponents.py --prefix ${prefix} --segid ${segid} --column ${counter} --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,423K,450K}/${i}/segregationIndex.dat

        counter=$((counter+1))
    done
done

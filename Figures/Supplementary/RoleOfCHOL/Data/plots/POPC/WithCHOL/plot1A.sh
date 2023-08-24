#!/bin/bash

WORKDIR=../../../analysis
SCRIPTDIR=../../scripts
SYSTEM=POPC

for i in 1 # 2 3 4
do
    prefix=${i}${SYSTEM}

    # python3 ${SCRIPTDIR}/plot_BSE.py --prefix ${prefix} --column 0 --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/binaryShannonEntropy.dat

    python3 ${SCRIPTDIR}/plot_CHE.py --prefix ${prefix} --column 0 --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/cumulativeHardEnrichment.dat

    python3 ${SCRIPTDIR}/plot_SegIndex.py --prefix ${prefix} --column 0 --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/segregationIndex.dat

    # python3 ${SCRIPTDIR}/plot_DBSCANsystemClusterCount.py --prefix ${prefix} --column 0 --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/DBSCANanalysisSystem.dat
    # python3 ${SCRIPTDIR}/plot_DBSCANsystemCore2Total.py --prefix ${prefix} --column 1 --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/DBSCANanalysisSystem.dat
    python3 ${SCRIPTDIR}/plot_DBSCANsystemLipids2Total.py --prefix ${prefix} --column 2 --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/DBSCANanalysisSystem.dat
    # python3 ${SCRIPTDIR}/plot_DBSCANsystemOutliers2Total.py --prefix ${prefix} --column 3 --dat_files ${WORKDIR}/data/${SYSTEM}/{298K,323K,450K}/${i}/DBSCANanalysisSystem.dat

done

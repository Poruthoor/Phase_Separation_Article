#!/bin/bash

###############################################################################
#                                                                             #
# Usage :                                                                     #
#   bash deleteSegIDfromList.sh SegID                                         #   
#                                                                             #
# Note : SegID keyword should match the segid in model file. Else, things can # 
#        can go haywire downstream                                            #
#                                                                             #
#        Provided a segID file and the segID to be removed (for example, we   #
#        know that CHOL does not make much of a difference when calculating   #
#        segregation index), this script go through all the DIPC, DAPC, POPC  #
#        system and replica folders to replace the existing `lipidList.dat`   #
#        to convert into `lipid_NO_${SPECIES}.dat` after removing the species #
#        details corresponding to the segID given. Everything is hardcoded in #
#        this script as this is mostly for one time use.                      #
#                                                                             #
###############################################################################

CURRENT=$PWD
SPECIES=$1

for SYSTEM in DAPC DIPC POPC
do
    rm -rf ${CURRENT}/${SYSTEM}/*/avgRcutoff_NO_${SPECIES}.dat
    rm -rf ${CURRENT}/${SYSTEM}/lipidList_NO_${SPECIES}.dat

    lipidList=${CURRENT}/${SYSTEM}/lipidList.dat

    # Removing the line corresponding where species keyword is found and
    # creating a new file without the species info
    sed "/${SPECIES}/d" ${lipidList} > ${CURRENT}/${SYSTEM}/lipidList_NO_${SPECIES}.dat

    for i in 298K 323K 333K 343K 353K 423K 450K
    do
        avgRcutoffFile=${CURRENT}/${SYSTEM}/${i}/avgRcutoff.dat

        sed "/${SPECIES}/d" ${avgRcutoffFile} > ${CURRENT}/${SYSTEM}/${i}/avgRcutoff_NO_${SPECIES}.dat

    done
done

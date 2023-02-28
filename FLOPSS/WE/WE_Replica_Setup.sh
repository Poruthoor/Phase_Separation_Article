#!/bin/bash

###############################################################################
# Usage                                                                       #
#                                                                             #
# WE_Replica_Setup.sh Num_Bstates Steps_btw > WE_Replica_Setup.out            #
#                                                                             #
#   Arguments :                                                               #
#               Num_States      : No. of frames to be taken from a trajectory.#
#               This traj correspond to a particular Temperature simulation   #
#               of a single replica [int]                                     #
#               Steps_btw       : No. of steps between two successive frames  #
#               to be captured [int]                                          #
#                                                                             #
#               NOTE : The frames are captured from the last frame and        #
#               backwards ( in reverse order)                                 #
#               to be captured [int]                                          #
#                                                                             #
# Example                                                                     #
#                                                                             #
# bash WE_Replica_Setup.sh 10 100 > WE_Replica_Setup.out                      #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD

###############################################################################
#             1. PREPARING INITIAL REPLICATES FOR BOTH DIPC & DAPC            #
###############################################################################

for i in DAPC # DIPC
do
    echo $i
    for j in 1 2 3 4
    do
        # Creating dir bstates for each replica run
        mkdir -pv $CURRENT/DPPC_${i}_CHOL/$j/bstates/
        # Creating dir common_files for each replica run
        mkdir -pv $CURRENT/DPPC_${i}_CHOL/$j/common_files/

        DEST=$CURRENT/DPPC_${i}_CHOL/$j/bstates
        DEST_CM=$CURRENT/DPPC_${i}_CHOL/$j/common_files

        # Set up a counter to make sure we have right number of bstates created
        COUNTER=0

        for k in 298K 323K 423K 450K 
        do
            cd ~/Phase_Seperation/restrained_memb/DPPC_${i}_CHOL/${j}/gromacs/Production/${k}/

            # Copying the dynamics files to /common_files. This has to be done
            # only once since they are common within a replica
            if [[ $COUNTER -eq 0 ]]
            then
                cp -p system.top $DEST_CM/
                cp -p index.ndx $DEST_CM/
                cp -p ref_system_centered.pdb $DEST_CM/
                cp -pr toppar $DEST_CM/

                # Creating a TEMPorary folder for creating bstates.txt
                mkdir -pv $DEST/TEMP
                cd /Ashlin2/ashlin/Phase_Seperation/Analysis/Trajectory/${i}/${j}/${k}/
                cp -p $j${i}.psf $DEST/TEMP/model.psf

            fi

            cd /Ashlin2/ashlin/Phase_Seperation/Analysis/Trajectory/${i}/${j}/${k}/

            for l in $(seq 0 $(($1-1)))
            do
                # Capture frames into pdb. Note that frames are captured in
                # reverse order
                if [[ $l -eq 0 ]]
                then
                    frame2pdb -- $j${i}.psf fixed_$j${i}.dcd -1 > ${DEST}/${j}${i}_${k}_frame_1.pdb
                else
                    frame2pdb -- $j${i}.psf fixed_$j${i}.dcd -$(($l*$2)) > ${DEST}/${j}${i}_${k}_frame_$(($l*$2)).pdb
                fi

            done

            cd $CURRENT/
            COUNTER=$(($COUNTER+1))
        done

        # No. of bstates in bstates/ dir. 
        FILENUM=$(ls -p $DEST/ | grep -v / | wc -l)

        if [[ $FILENUM  -eq  $(($COUNTER*$1)) ]]
        then
            # Total no. of bstates that should be inside bstates/ dir
            TOTAL=$(($COUNTER*$1))
            # Probability of each file to be randomly chosen
            PROB=$(echo "scale=5 ;1 / $TOTAL" | bc)

            # Parsing filenames in the dir to a file
            ls -p $DEST/ | grep -v / > $DEST/TEMP/filename.txt
            # Parsing the line number into a file
            seq 0 $(($TOTAL-1)) > $DEST/TEMP/num.txt
            # Parsing probabilities to a file
            yes "$PROB" | head -$TOTAL > $DEST/TEMP/prob.txt
            # Finally formatting bstates.txt the right way in columns
            paste $DEST/TEMP/num.txt $DEST/TEMP/prob.txt $DEST/TEMP/filename.txt > $DEST/bstates.txt

            # Bringing back .psf files to bstates/
            mv $DEST/TEMP/model.psf $DEST/model.psf

            # We don't need TEMP/ anymore
            rm -rf $DEST/TEMP
        fi
    done
done
###############################################################################

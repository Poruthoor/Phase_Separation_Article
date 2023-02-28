#!/bin/bash

###############################################################################
#                                                                             #
# Usage :                                                                     #
#                                                                             #
#   bash xy_rdfFromReplica.sh lipidList model traj1 traj2 ...                 #   
#                                                                             #
# Disclaimer : You need to install LOOS in your env                           # 
#                                                                             #
# Notes:                                                                      #
#                                                                             #
#    Calculates xy_rdf for the species mentioned in lipidList, for all the    #
#    trajectories given in the input arguments, provided adequate model file  #
#    is given.                                                                #
#                                                                             #
#    This is a precursor to the `xy_rdfBTWlikeSegments.sh` script.            #  
#                                                                             #
#    For each species given in the lipidList file, this script calculates     #
#    xy_rdf between same species segIDs and creates a `.xyRDF` file with      #
#    appropriate filename. Neither time-step range feature nor the reselect   #
#    feature is available in this script.                                     #
#                                                                             #
###############################################################################

lipidList=$1
model=$2

echo "File from segid are taken : ${lipidList}"
echo "Model File used : ${model}"

counter=0
for traj in "$@"
do
    if [ $counter -gt 1 ]
    then
        echo "Calculating xy RDF for trajectory file : "$traj""
        trajFileName=$(basename -- "$traj")
        extension="${trajFileName##*.}"
        prefix=$(basename "${trajFileName}" ."${extension}")
        while read lipid
        do
            xy_rdf $model $traj  'segid == "'${lipid}'"' \
                'segid == "'${lipid}'"' 0 40 40 \
                --split-mode=by-molecule > ${prefix}_${lipid}-${lipid}.xyRDF
            echo ""$lipid" - "$lipid" Done."
        done<$lipidList
    fi
    counter=$((counter+1))
done


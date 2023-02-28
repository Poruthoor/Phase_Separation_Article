#!/bin/bash

###############################################################################
#                                                                             #
# Usage :                                                                     #
#                                                                             #
#   bash xy_rdfBTWlikeSegments.sh lipidList model traj range                  #   
#                                                                             #
#   Notes:                                                                    #
#                                                                             #
#     Calculates xy_rdf between like-segments in a trajectory file for given  #
#     model file and time-step range.                                         #
#                                                                             #
#     This script have four input arguments:                                  #
#                                                                             #
#         LipidList   : A file consisting of all the information about        #
#                       (lipids) segID that to be included in the analysis    #
#                       protocol. File syntax should be identical to that of  #
#                       `lipidList.dat`                                       #
#                                                                             #
#         model       : Path to LOOS supported model file (Ex:`.psf`,`.pdb`)  #
#                                                                             #
#         traj        : Path to LOOS supported traj file                      #
#                                                                             #
#         range       : Time step `range` over which, the xy_rdf should be    #
#                       calculated is defined for each system.                #
#                                                                             #
#     For the each species in the lipidList, xy_rdf is calculated between     #
#     like species. Here, histogram binning min and max distance is hard      #
#     capped between 0 and 40 A. Number of bins is capped at 40 to have a     #
#     bin width of 1 A - This is hardcoded as well. Since, we have CHOL,      #
#     lipid leaflet location is recomputed every frame using `--reselect`     #
#     flag. This wont be necessary if your system does not have leaflets      #
#     or species that flipflops across leaflets. For more info on the xy_rdf  #
#     arguments, please see `xy_rdf --fullhelp`                               #
#                                                                             #
#     The prefix for the output file is obtained from traj filename, the      #
#     suffix                                                                  #
#     is the segment-segment name over which xy_rdf was calculated. The       #
#     output                                                                  #
#     file extension is `.xyRDF`                                              #
#                                                                             #
# Disclaimer : You need to install LOOS in your env                           # 
###############################################################################

lipidList=$1
model=$2
traj=$3
range=$4

echo "File from segid are taken : ${lipidList}"
echo "Model File used : ${model}"

echo "Calculating xy RDF for trajectory file : "$traj""
trajFileName=$(basename -- "$traj")
extension="${trajFileName##*.}"
prefix=$(basename "${trajFileName}" ."${extension}")
while read lipid
do
    xy_rdf $model $traj  'segid == "'${lipid}'"' \
        'segid == "'${lipid}'"' 0 40 40 \
        --range $range  \
        --split-mode=by-molecule \
        --reselect > ${prefix}_${lipid}-${lipid}.xyRDF
    echo ""$lipid" - "$lipid" Done."
done<$lipidList

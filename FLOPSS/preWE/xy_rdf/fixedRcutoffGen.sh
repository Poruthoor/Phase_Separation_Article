#!/bin/bash

###############################################################################
#                                                                             #
# Usage:                                                                      #
#    bash fixedRcutoffGen.sh PATH/To/lipidList/File fixedRcutoff              #
#                                                                             #
# Example:                                                                    #
#    bash fixedRcutoffGen.sh DAPC/lipidList.dat 13                            #
#                                                                             #
# Notes:                                                                      #
#                                                                             #
#    Outputs a file equivalent to that of   `avrRcutoff.sh` but with given    #
#    fixed radius. This can be used if you are sure that nearest neighbor     #
#    radius for all your species in the lipid list are same and does not      #
#    matter. Or you can use it to debug.                                      #
#                                                                             #
###############################################################################

lipidList=$1
output=$(basename -- "$1")

awk -v fixedR=$2 '{print $0, fixedR}' $lipidList > fixedR_$output

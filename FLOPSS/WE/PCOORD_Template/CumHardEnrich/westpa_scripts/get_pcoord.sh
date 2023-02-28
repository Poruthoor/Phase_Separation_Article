#!/bin/bash
#
# get_pcoord.sh
#
# This script is run when calculating initial progress coordinates for new
# initial states (istates).  This script is NOT run for calculating the progress
# coordinates of most trajectory segments; that is instead the job of runseg.sh.

# If we are debugging, output a lot of extra information.
if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

# Make sure we are in the correct directory
cd $WEST_SIM_ROOT/common_files

############################## Progress Coord ################################# 

# Creating a temporary file to store pcoord
TEMP=$(mktemp)

# Set the arguments for Contacts2D.py and call the script to calculate initial
# progress coordinate.

python3 $WEST_SIM_ROOT/common_files/cumulativeHardEnrichment.py \
    --model $WEST_SIM_ROOT/bstates/model.psf \
    --traj $WEST_STRUCT_DATA_REF \
    --lipid_list $WEST_SIM_ROOT/common_files/lipidList.dat \
    --r $WEST_SIM_ROOT/common_files/avgRcutoff.dat > $TEMP

cat $TEMP | tail -n +3 | awk {'print $1'} > $WEST_PCOORD_RETURN
cat $TEMP | tail -n +3 | awk {'print $2'} > $WEST_DPPC_RETURN
cat $TEMP | tail -n +3 | awk {'print $3'} > $WEST_DXPC_RETURN
cat $TEMP | tail -n +3 | awk {'print $4'} > $WEST_CHOL_RETURN

# Clean up
rm -f $TEMP

###############################################################################

if [ -n "$SEG_DEBUG" ] ; then
  head -v $WEST_PCOORD_RETURN
fi

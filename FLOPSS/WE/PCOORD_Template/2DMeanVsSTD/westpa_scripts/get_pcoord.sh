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
TEMP_SPECIES=$(mktemp)

# Set the arguments for Contacts2D.py and call the script to calculate initial
# progress coordinate.

python3 $WEST_SIM_ROOT/common_files/wDBSCANanalysisSpecies.py \
    --model $WEST_SIM_ROOT/bstates/model.psf \
    --traj $WEST_STRUCT_DATA_REF \
    --lipid_list $WEST_SIM_ROOT/common_files/lipidList.dat \
    --r $WEST_SIM_ROOT/common_files/avgRcutoff.dat > $TEMP

paste <(cat $TEMP | tail -n +4 | awk {'print $2'}) <(cat $TEMP | tail -n +4 | awk {'print $5'}) > $WEST_PCOORD_RETURN
paste <(cat $TEMP | tail -n +4 | awk {'print $1'}) <(cat $TEMP | tail -n +4 | awk {'print $4'}) > $WEST_DPPC_RETURN
paste <(cat $TEMP | tail -n +4 | awk {'print $3'}) <(cat $TEMP | tail -n +4 | awk {'print $6'}) > $WEST_CHOL_RETURN

cat $TEMP | tail -n +4 | awk {'print $7'} > $WEST_SILCOEFFDPPC_RETURN
cat $TEMP | tail -n +4 | awk {'print $8'} > $WEST_SILCOEFFDXPC_RETURN
cat $TEMP | tail -n +4 | awk {'print $9'} > $WEST_SILCOEFFCHOL_RETURN

python3 $WEST_SIM_ROOT/common_files/DBSCANanalysisSpecies.py \
    --model $WEST_SIM_ROOT/bstates/model.psf \
    --traj $WEST_STRUCT_DATA_REF \
    --lipid_list $WEST_SIM_ROOT/common_files/lipidList.dat \
    --r $WEST_SIM_ROOT/common_files/avgRcutoff.dat > $TEMP_SPECIES

cat $TEMP_SPECIES | tail -n +4 | awk {'print $1'} > $WEST_CLUCOUNTDPPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $2'} > $WEST_CLUCOUNTDXPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $3'} > $WEST_CLUCOUNTCHOL_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $4'} > $WEST_COREBYDPPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $5'} > $WEST_COREBYDXPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $6'} > $WEST_COREBYCHOL_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $7'} > $WEST_CLUSBYDPPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $8'} > $WEST_CLUSBYDXPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $9'} > $WEST_CLUSBYCHOL_RETURN

# Clean up
rm -f $TEMP $TEMP_SPECIES

###############################################################################

if [ -n "$SEG_DEBUG" ] ; then
  head -v $WEST_PCOORD_RETURN
fi

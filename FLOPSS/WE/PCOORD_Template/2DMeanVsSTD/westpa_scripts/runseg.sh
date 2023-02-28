#!/bin/bash
#
# runseg.sh
#
# WESTPA runs this script for each trajectory segment. WESTPA supplies
# environment variables that are unique to each segment, such as:
#
#   WEST_CURRENT_SEG_DATA_REF: A path to where the current trajectory segment's
#       data will be stored. This will become "WEST_PARENT_DATA_REF" for any
#       child segments that spawn from this segment
#   WEST_PARENT_DATA_REF: A path to a file or directory containing data for the
#       parent segment.
#   WEST_CURRENT_SEG_INITPOINT_TYPE: Specifies whether this segment is starting
#       anew, or if this segment continues from where another segment left off.
#   WEST_RAND16: A random integer
#
# This script has the following four jobs:
#  1. Create a directory for the current trajectory segment, and set up the
#     directory for running MD engine
#  2. Determine whether the child traj should eihter continue from an existing
#     parent tractory, or start a new trajectory. In the latter case, we need 
#     to do a couple things differently, such as generating velocities.
#  3. Run the dynamics
#  4. Calculate the progress coordinates and return data to WESTPA

# If we are running in debug mode, then output a lot of extra information.
if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

################################ For multi GPU #################################

export CUDA_VISIBLE_DEVICES=$WM_PROCESS_INDEX

######################## Set up for running the dynamics #######################

# Set up the directory where data for this segment will be stored.
cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

# Make symbolic links to the files necessary for GROMACS MD engine but are not
# unique to each segment.
mkdir -pv toppar
ln -sv $WEST_SIM_ROOT/common_files/toppar/*.itp toppar/
ln -sv $WEST_SIM_ROOT/common_files/system.top .
ln -sv $WEST_SIM_ROOT/common_files/index.ndx .
ln -sv $WEST_SIM_ROOT/common_files/md.mdp .
# If the system has constraints, link reference files for GROMACS as well. Else
# following symbolic is not necessary for a standard GROMACS MD run.
ln -sv $WEST_SIM_ROOT/common_files/ref_system_centered.pdb .

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then

    ln -sv $WEST_PARENT_DATA_REF/seg.cpt ./parent.cpt
    ln -sv $WEST_PARENT_DATA_REF/seg.pdb ./parent.pdb
    # A continuation from a prior segment
    gmx grompp -f md.mdp -o seg.tpr -c parent.pdb -r ref_system_centered.pdb \
        -t parent.cpt -p system.top -n index.ndx -po md_out.mdp -maxwarn 2 || exit 1

elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then

    ln -sv $WEST_PARENT_DATA_REF ./parent.pdb
    # Initiation of a new trajectory; $WEST_PARENT_DATA_REF contains the reference to the
    # appropriate basis state or generated initial state
    gmx grompp -f md.mdp -o seg.tpr -c parent.pdb -r ref_system_centered.pdb \
        -p system.top -n index.ndx -po md_out.mdp -maxwarn 2 || exit 1

else

    # This should never fire.
    echo "unknown init point type $WEST_CURRENT_SEG_INITPOINT_TYPE"
    exit 2

fi

############################## Run the dynamics ################################

# Propagate segment using MD engine
gmx mdrun -nt 1 -deffnm seg -cpo seg.cpt -c seg.pdb

# Post processing the trajectory - reimaging and centering using LOOS 
subsetter -C 'resname =~ "PC" || resname == "CHOL"' \
    --reimage=extreme traj $WEST_SIM_ROOT/bstates/model.psf seg.xtc

############################## Progress Coord ################################# 

# Creating a temporary file to store pcoord
TEMP=$(mktemp)
TEMP_SPECIES=$(mktemp)

# Set the arguments for PCOORD.py and call the script to calculate initial
# progress coordinate.

python3 $WEST_SIM_ROOT/common_files/wDBSCANanalysisSpecies.py \
    --model $WEST_SIM_ROOT/bstates/model.psf \
    --traj traj.dcd \
    --lipid_list $WEST_SIM_ROOT/common_files/lipidList.dat \
    --r $WEST_SIM_ROOT/common_files/avgRcutoff.dat > $TEMP || exit 1

paste <(cat $TEMP | tail -n +4 | awk {'print $2'}) <(cat $TEMP | tail -n +4 | awk {'print $5'}) > $WEST_PCOORD_RETURN
paste <(cat $TEMP | tail -n +4 | awk {'print $1'}) <(cat $TEMP | tail -n +4 | awk {'print $4'}) > $WEST_DPPC_RETURN
paste <(cat $TEMP | tail -n +4 | awk {'print $3'}) <(cat $TEMP | tail -n +4 | awk {'print $6'}) > $WEST_CHOL_RETURN

cat $TEMP | tail -n +4 | awk {'print $7'} > $WEST_SILCOEFFDPPC_RETURN
cat $TEMP | tail -n +4 | awk {'print $8'} > $WEST_SILCOEFFDXPC_RETURN
cat $TEMP | tail -n +4 | awk {'print $9'} > $WEST_SILCOEFFCHOL_RETURN

python3 $WEST_SIM_ROOT/common_files/DBSCANanalysisSpecies.py \
    --model $WEST_SIM_ROOT/bstates/model.psf \
    --traj traj.dcd \
    --lipid_list $WEST_SIM_ROOT/common_files/lipidList.dat \
    --r $WEST_SIM_ROOT/common_files/avgRcutoff.dat > $TEMP_SPECIES || exit 1

cat $TEMP_SPECIES | tail -n +4 | awk {'print $1'} > $WEST_CLUCOUNTDPPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $2'} > $WEST_CLUCOUNTDXPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $3'} > $WEST_CLUCOUNTCHOL_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $4'} > $WEST_COREBYDPPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $5'} > $WEST_COREBYDXPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $6'} > $WEST_COREBYCHOL_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $7'} > $WEST_CLUSBYDPPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $8'} > $WEST_CLUSBYDXPC_RETURN
cat $TEMP_SPECIES | tail -n +4 | awk {'print $9'} > $WEST_CLUSBYCHOL_RETURN

###############################################################################

# Clean up
rm -f *.mdp *.ndx *.top ref_system_centered.pdb *.gro traj.dcd traj.pdb $TEMP $TEMP_SPECIES
rm -rf toppar

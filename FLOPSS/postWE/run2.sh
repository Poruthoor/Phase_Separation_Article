#! /bin/bash

# conda deactivate
# conda activate westpa-2020.02

# Sanity check #2
echo "Sanity check #2"
# Flux Analysis : Calculate the flux and state populations.
echo "Flux Analysis : Calculate the flux and state populations.(2/2)"
cd fluxAnalysis/
bash run.sh
cd ..
echo "Done!(2/2)"

##------------------------------------------------##

# Constructing FES using auxillary variables stored in .h5 file
sbatch otherFES/Analysis.sh
# bash otherFES/Analysis_DAPC.sh
# bash otherFES/Analysis_DIPC.sh
# bash otherFES/Analysis_POPC.sh

# Combining multiple replica using multi_west
conda deactivate
conda activate westpa-2020.05

#########################################
# WARNING! MIGHT NEED MANUAL INTERVENTION
# CHECK THE COMMENTS INSIDE THE SCRIPT
#########################################
sbatch multiWest/combine.sh
#########################################

bash multiWest/pdist2data_multi.sh

# Make sure you updated the otherFES/module.py before next step

bash otherFES/Analysis_multi.sh

##------------------------------------------------##

## PLEASE read the reweighOverOtherCVs/README.md before proceeding further. 

## Reweighting over other Auxillary coordinate that was not planned
conda deactivate
conda activate westpa-2020.05

# After transfering fakeWE folders into respective directories
# Make the necessary file tree for combining multiple replica
sbatch reweighOverOtherCVs/makeFileTree.sh

#########################################
# WARNING! MIGHT NEED MANUAL INTERVENTION
# CHECK THE COMMENTS INSIDE THE SCRIPT
#########################################
sbatch reweighOverOtherCVs/combine.sh
#########################################

bash reweighOverOtherCVs/pdist2data_multi.sh

# Make sure you updated the reweighOverOtherCVs/module.py before next step
sbatch otherFES/Analysis_ReweighOverOtherCVs_multi.sh

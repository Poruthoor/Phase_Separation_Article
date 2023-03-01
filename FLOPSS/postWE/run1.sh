#! /bin/bash

conda deactivate
conda activate westpa-2020.02

# # Run initial data pull from the WE simulation and make cv evolution .pdf files.
echo "Run initial data pull from the WE simulation and make cv evolution .pdf files."
# bash west2pdist/Analysis_DAPC.sh
# bash west2pdist/Analysis_DIPC.sh
# bash west2pdist/Analysis_POPC.sh
sbatch west2pdist/Analysis.sh
echo "Done!"

# # Process the pdist.h5 
echo "Process the pdist.h5" 
sbatch pdist2data/pdist2data_DAPC.sh
sbatch pdist2data/pdist2data_DIPC.sh
sbatch pdist2data/pdist2data_POPC.sh
echo "Done!"

# Sanity check #1
echo "Sanity check #1"
# Compare FES from vanilla simulations and their corresponding WE simulations.
echo "Compare FES from vanilla simulations and their corresponding WE simulations."
bash sanityCheck/Vanilla_files_transfer.sh
bash sanityCheck/WE_files_transfer.sh
echo "Done!"

# Sanity check #2
echo "Sanity check #2"
# Flux Analysis : Calculate the flux and state populations.
echo "Flux Analysis : Calculate the flux and state populations.(1/2)"
cd fluxAnalysis/
sbatch flux_DAPC.sh
sbatch flux_DIPC.sh
# sbatch flux_POPC.sh
cd ../
echo "Done!(1/2)"
echo "Execute run2.sh, to continue with the 2/2 stage of flux analysis"

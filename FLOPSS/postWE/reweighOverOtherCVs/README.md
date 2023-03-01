# In our case, we transfered most WE sims into local machine we had to do
# the following step 0 in addition. Else skip to step 1 and ignore step 3.

# STEP 0
# Since we took all the files into local machine, and split into various
# harddisks, we need a place where all traj data are present.
# The following script does that for you. Again, it works for my file tree
# struture but not necessarily for yours as yours may be different. Plus, you
# don't have to use it, if you have last 10 WE iteration data in the
# supercomputing cluster. 

bash createSymLink.sh

# STEP 1
# Copy necessary CV scripts and python scripts to execute them into respective
# WE folder. Feel free to deposit any new scripts that you want to execute in
# each folder like new CVs inside the `copy2MainWEdir/` folder

bash copy2MainWEdir.sh

# STEP 2
# Now you have to cd into individual Replica folder and do the rest
# in each dir

conda activate loos
nohup bash generateAuxDataFast.sh -a auxList.txt -f 490 -l 500 &
# nohup bash generateAuxDataFast.sh -a auxList.txt -f 250 -l 500 &
nohup bash parseAuxData.sh &

# STEP 3
# Once done with all the folders, use the following script to transfer the
# files back to Bluehive. Again, this is only if you are transfering files back
# into cluster

cd /Ashlin5/ashlin/Phase_Seperation/Weighted_Ensemble_3/transfer/
bash rsync_BHV.sh

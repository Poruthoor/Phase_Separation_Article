

# To plot the all possible FLC cutoff with data points across the temperatures considered in the input dat_file argument
# This script outputs 2 plots : One is del del G vs FLC cutoff --> Gives you a better idea about FLC cutoff sensitivity
# The other would be the regular del del G vs Temperature
python3 delGvsCV.py --cv ClusterLipids2Total --suffix DIPC_Multi --xLabel FLC --dat_files DPPC_DIPC_CHOL/{298,323,353}K/multi_west/*average_490-500.dat
python3 delGvsCV.py --cv ClusterLipids2Total --suffix DAPC_Multi --xLabel FLC --dat_files DPPC_DAPC_CHOL/{298,323,333,343,353,373,423}K/multi_west/*average_490-500.dat

# Once we settle on a cutoff, you can use the cutoff argument to extract just one FLC cutoff plot - the plot will be
# empty if there there's an infinite/nan for the del del G in any one of the temperature being considered in the files
# you gave as input. This is a very strict condition that I'm enforcing and can be changed in the ploting script.
python3 delGvsCV.py --cv ClusterLipids2Total --suffix DIPC_Multi_cutoff --cutoff 0.6 --xLabel FLC --dat_files DPPC_DIPC_CHOL/{298,323,353}K/multi_west/*average_490-500.dat
python3 delGvsCV.py --cv ClusterLipids2Total --suffix DAPC_Multi_cutoff --cutoff 0.6 --xLabel FLC --dat_files DPPC_DAPC_CHOL/{298,323,333,343,353,373,423}K/multi_west/*average_490-500.dat

# Just to get a .asc file containg temperature and del2G
python3 delGvsT.py --cv ClusterLipids2Total --suffix DAPC_Multi --cutoff 0.6 --dat_files DPPC_DAPC_CHOL/{298,323,333,343,353,373,423}K/multi_west/*average_490-500.dat
python3 delGvsT.py --cv ClusterLipids2Total --suffix DIPC_Multi --cutoff 0.6 --dat_files DPPC_DIPC_CHOL/{298,323,353}K/multi_west/*average_490-500.da

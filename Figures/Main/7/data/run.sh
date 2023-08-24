# Just to get a .asc file containg temperature and del2G
python3 delGvsT.py --cv ClusterLipids2Total --suffix DAPC_Multi --cutoff 0.625 --dat_files DPPC_DAPC_CHOL/{298,323,333,343,353,373,423}K/multi_west/*average_490-500.dat
python3 delGvsT.py --cv ClusterLipids2Total --suffix DIPC_Multi --cutoff 0.525 --dat_files DPPC_DIPC_CHOL/{298,323,353}K/multi_west/*average_490-500.dat

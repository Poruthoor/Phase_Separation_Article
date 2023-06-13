python3 multi_last.py --cv ClusterLipids2Total --suffix POPC_multi --xRange "(0, 1)" --yRange "(0, 5)" --xLabel FLC --dat_files POPC/{298,450}K/*average_*.dat
python3 multi_last.py --cv ClusterLipids2Total --suffix DAPC_multi --xRange "(0, 1)" --yRange "(0, 5)" --xLabel FLC --dat_files DAPC/{298,323,353,423}K/*average_*.dat
python3 multi_last.py --cv ClusterLipids2Total --suffix DIPC_multi --xRange "(0, 1)" --yRange "(0, 5)" --xLabel FLC --dat_files DIPC/{298,323,353,423}K/*average_*.dat

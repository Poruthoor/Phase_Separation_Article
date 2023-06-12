# WESTPA pdist.h5 files to data files
python3 evolution.py --suffix FLC --temperature 323 --plotscale energy --dat_file ClusterLipids2Total/DPPC_DIPC_CHOL/323K/1/pdist.h5
python3 evolution.py --suffix CEI --temperature 323 --plotscale energy --dat_file CumHardEnrich/DPPC_DIPC_CHOL/323K/1/pdist.h5
python3 evolution.py --suffix SI --temperature 323 --plotscale energy --dat_file SegIndex/DPPC_DIPC_CHOL/323K/1/pdist.h5
# Ploting
python3 plot_evolution.py --cv FLC --prefix DIPC_323K --blocked_iter test_iterationBlock.dat --midpoint test_pcoordMidpoint.dat --plotHist test_plotHist.dat --plotScale energy --xLo 0 --xUp 1 --zUp 5
python3 plot_evolution.py --cv SI --prefix DIPC_323K --blocked_iter SI_iterationBlock.dat --midpoint SI_pcoordMidpoint.dat --plotHist SI_plotHist.dat --plotScale energy --xLo 0.8 --xUp 2 --zUp 5
python3 plot_evolution.py --cv CEI --prefix DIPC_323K --blocked_iter CEI_iterationBlock.dat --midpoint CEI_pcoordMidpoint.dat --plotHist CEI_plotHist.dat --plotScale energy --xLo 3 --xUp 6 --zUp 5

cp -prf west.h5 fakeWEfolder/westAux.h5

# Control
python3 reweighOverOtherCVs.py --WEdir . --auxLabel pcoord --first 490 --last 500

# CHE for the system
python3 reweighOverOtherCVs.py --WEdir . --auxLabel CHE --first 490 --last 500

# CHE for each species in the system
python3 reweighOverOtherCVs.py --WEdir . --auxLabel CHE --first 490 --last 500 --species DPPC
python3 reweighOverOtherCVs.py --WEdir . --auxLabel CHE --first 490 --last 500 --species DXPC
python3 reweighOverOtherCVs.py --WEdir . --auxLabel CHE --first 490 --last 500 --species CHOL

# SI for the system
python3 reweighOverOtherCVs.py --WEdir . --auxLabel SI --first 490 --last 500

# SI for each species in the system
python3 reweighOverOtherCVs.py --WEdir . --auxLabel SI --first 490 --last 500 --species DPPC
python3 reweighOverOtherCVs.py --WEdir . --auxLabel SI --first 490 --last 500 --species DXPC
python3 reweighOverOtherCVs.py --WEdir . --auxLabel SI --first 490 --last 500 --species CHOL

# SI for the system without considering CHOL
python3 reweighOverOtherCVs.py --WEdir . --auxLabel SI_WithoutCHOL --first 490 --last 500

# SI for each species in the system without considering
# CHOL
python3 reweighOverOtherCVs.py --WEdir . --auxLabel SI_WithoutCHOL --first 490 --last 500 --species DPPC
python3 reweighOverOtherCVs.py --WEdir . --auxLabel SI_WithoutCHOL --first 490 --last 500 --species DXPC

# 2D Aux coord that calculate mean lipids in cluster vs std
# of lipids in cluster (both weighted by the core lipids in
# each cluster)
python3 reweighOverOtherCVs.py --WEdir . --auxLabel weightedCluster --first 490 --last 500 --species DPPC --aux2D True
python3 reweighOverOtherCVs.py --WEdir . --auxLabel weightedCluster --first 490 --last 500 --species DXPC --aux2D True
python3 reweighOverOtherCVs.py --WEdir . --auxLabel weightedCluster --first 490 --last 500 --species CHOL --aux2D True

# MOPS for each species in the system
python3 reweighOverOtherCVs.py --WEdir . --auxLabel mops --first 490 --last 500 --species DPPC
python3 reweighOverOtherCVs.py --WEdir . --auxLabel mops --first 490 --last 500 --species XXXX
python3 reweighOverOtherCVs.py --WEdir . --auxLabel mops --first 490 --last 500 --species CHOL

# 2D Aux coord that calculate mean lipids in cluster vs std
# of lipids in cluster (both weighted by the core lipids in
# each cluster)
python3 reweighOverOtherCVs.py --WEdir . --auxLabel mops2D --first 490 --last 500 --species DPPC --aux2D True
python3 reweighOverOtherCVs.py --WEdir . --auxLabel mops2D --first 490 --last 500 --species XXXX --aux2D True
python3 reweighOverOtherCVs.py --WEdir . --auxLabel mops2D --first 490 --last 500 --species CHOL --aux2D True

# DBSCAN fixed r cutoff with minimum cluster min_dist
python3 reweighOverOtherCVs.py --WEdir . --auxLabel DBSCAN_fixed_min --first 490 --last 500

# DBSCAN fixed r cutoff with maximum cluster min_dist
python3 reweighOverOtherCVs.py --WEdir . --auxLabel DBSCAN_fixed_max --first 490 --last 500

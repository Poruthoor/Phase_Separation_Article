# #!/bin/bash

# ###############################################################################
# #                                                                             #
# # Assumes that there exist DAPC DIPC POPC dirs with respective lipidList.dat, #
# # consisting of lipid segment info, inside each dirs                          #
# #                                                                             #
# ###############################################################################

# # If you want to have cutoff radius defined by the XY-RDF method
# bash xy_rdfAcrossAll.sh
# bash avgRcutoff.sh

# # If you want to have fixed cutoff radius use fixedRcutoffGen.sh

# # Plot r cutoff vs Temp and create min and max average r cutoff files for
# # post-weighting with DBSCAN fixed cutoff analysis

CURRENT=$PWD

for SYSTEM in DAPC DIPC POPC
do
    cd ${SYSTEM}/

    rm -rf *m*_avgRcutoff.dat
    python3 ${CURRENT}/plot_avgRcutoff.py --suffix ${SYSTEM} --yRange "(10,30)" --dat_files ${CURRENT}/${SYSTEM}/*K/avgRcutoff.dat --extraOut min > min_avgRcutoff.dat
    python3 ${CURRENT}/plot_avgRcutoff.py --suffix ${SYSTEM} --yRange "(10,30)" --dat_files ${CURRENT}/${SYSTEM}/*K/avgRcutoff.dat --extraOut max > max_avgRcutoff.dat

    cd ${CURRENT}

done

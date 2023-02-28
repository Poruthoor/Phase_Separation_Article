#!/bin/bash

#####################################################################################################
#                                                                                                   #
#    Calculates xy_rdf across all the systems, temperatures and replicas hardcoded in the script.   #
#                                                                                                   #
#    This is a script that's being called from `run.sh`.                                            #
#                                                                                                   #
#    + It removes any xy_rdf data and reports generated by previous runs of this protocol.          #
#                                                                                                   #
#    + The `lipidList.dat` is taken as input - This is hardcoded as of now: A file consisting       #
#        of all the information about (lipids) segID that to be included in the analysis protocol.  #
#                                                                                                   #
#    + Time step `range` over which, the xy_rdf should be calculated is defined for each system.    #
#        As of now, this is hardcoded. For all system, this is 8 us. All the time steps beyond      #
#        this range is ignored even if it is present in the trajectory.                             #
#                                                                                                   #
#    + For each system, the corresponding temperature and replica, corresponding traj file and      #
#        model files are identified and corresponding folders are created to save xy_rdf data and   #
#        report.                                                                                    #
#                                                                                                   #
#    + xy_rdf calculation is done by calling another script : `xy_rdfBTWlikeSegments.sh`            #
#                                                                                                   #
#####################################################################################################

CURRENT=$PWD

for SYSTEM in DAPC DIPC POPC
do
    rm -rf ${SYSTEM}/*/*/xyRDF.report
    rm -rf ${SYSTEM}/*/*/*.xyRDF
    list=${CURRENT}/${SYSTEM}/lipidList.dat

    range=0:1:79

    for i in 298K 313K 323K 333K 343K 353K 373K 423K 450K
    do

       for j in 1 2 3 4 
       do

            traj=/localdata/ashlin/Phase_Seperation/Analysis/Trajectory/${SYSTEM}/${j}/${i}/fixed_${j}${SYSTEM}_100.dcd
            model=/localdata/ashlin/Phase_Seperation/Analysis/Trajectory/${SYSTEM}/${j}/${i}/${j}${SYSTEM}.psf

            if [ -s $traj ] && [ -s $model ]
            then

                mkdir -p ${SYSTEM}/${i}/${j}
                cd ${SYSTEM}/${i}/${j}/


                echo "Calculating xy-RDF for ${SYSTEM} : Replica ${j} at Temperature ${i}"

                echo "bash ${CURRENT}/xy_rdfBTWlikeSegments.sh ${list} ${model} ${traj} ${range}" >> xyRDF.report

                bash ${CURRENT}/xy_rdfBTWlikeSegments.sh ${list} ${model} ${traj} ${range}
            fi

            cd ${CURRENT}
        done
    done
done

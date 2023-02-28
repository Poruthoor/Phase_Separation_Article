#!/bin/bash

# Running following CV scripts that have similar input arguments. Hence the
# name Template 1. As you can see for all the CV scripts in this template
# requires a lipid list and cutoff radius to define a local region.

for analysis in binaryShannonEntropy cumulativeHardEnrichment segregationIndex
do
    bash analysisTemplate1.sh ${analysis}
done

for analysis in DBSCANanalysisSpecies DBSCANanalysisSystem
do
    bash analysisTemplate1.sh ${analysis}
done

for analysis in wDBSCANanalysisSpecies wDBSCANanalysisSystem
do
    bash analysisTemplate1.sh ${analysis}
done

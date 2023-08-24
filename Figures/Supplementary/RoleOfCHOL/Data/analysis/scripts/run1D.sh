#!/bin/bash

# Running following CV scripts that have similar input arguments. Hence the
# name Template 1. As you can see for all the CV scripts in this template
# requires a lipid list and cutoff radius to define a local region.

# WITH CHOLESTEROL

for analysis in cumulativeHardEnrichment segregationIndex
do
    bash analysisTemplate1.sh ${analysis}
done

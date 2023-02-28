#!/bin/bash

# Running following CV scripts that have similar input arguments. Hence the
# name Template 2. As you can see for all the CV scripts in this template
# requires a lipid list and cutoff radius to define a local region.

# WITHOUT CHOLESTEROL

for analysis in cumulativeHardEnrichment segregationIndex
do
    bash analysisTemplate2.sh ${analysis}
done

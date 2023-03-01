#! /bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo ""
   echo "Executes the auxillary CV script on the trajectory provided and
   returns the data into a file with given filename"
   echo
   echo "Usage: bash generateAuxData.sh [-h|t|f|p]"
   echo "options:"
   echo "-h     Display help."
   echo "-t     Path to the traj"
   echo "-f     File name."
   echo "-m     model file (.psf) path."
   echo "-r     radius cutoff File path."
   echo "-l     lipid List File path."
   echo
}

############################################################
############################################################
# Input Arguments                                          #
############################################################
############################################################

while getopts :t:f:m:r:l:h flag
do
    case "${flag}" in
        t) traj=${OPTARG};;
        f) fileName=${OPTARG};;
        m) model=${OPTARG};;
        r) rFile=${OPTARG};;
        l) lipidList=${OPTARG};;
        h) # Display Help
            Help
            exit;;
        \?) # Invalid option
            echo "Error: Invalid option"
            Help
            exit;;
    esac
done

# No arguments?
if [[ $# -eq 0 ]] ; then
    echo ""
    echo "Inputs needed !!"
    Help
    exit 0
fi

HEADDIR=/Ashlin5/ashlin/Phase_Seperation/Weighted_Ensemble_3/CVs4PhaseSeparation/

TEMP_SYSTEM=$(mktemp)

if [ -s $traj ] && [ -s $model ]
then

    python3 ${HEADDIR}/CVs/cumulativeHardEnrichment.py \
        --model ${model} \
        --traj ${traj} \
        --lipid_list ${lipidList} \
        --r ${rFile} >> $TEMP_SYSTEM || exit 1

    cat $TEMP_SYSTEM | tail -n +3 | awk {'print $1'} > ${fileName}.dat
    cat $TEMP_SYSTEM | tail -n +3 | awk {'print $2'} > ${fileName}_DPPC.dat
    cat $TEMP_SYSTEM | tail -n +3 | awk {'print $3'} > ${fileName}_DXPC.dat
    cat $TEMP_SYSTEM | tail -n +3 | awk {'print $4'} > ${fileName}_CHOL.dat
    
fi

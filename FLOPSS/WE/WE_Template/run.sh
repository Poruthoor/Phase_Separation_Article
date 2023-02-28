#!/bin/bash
#SBATCH --partition=gpu -C K20X
#SBATCH --gres=gpu:2
#SBATCH --time=120:00:00
#SBATCH --job-name=WESTPA_RUN
#SBATCH --output=WESTPA_RUN.out
#SBATCH --error=WESTPA_RUN.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24

###############################################################################
#                                                                             #
# run.sh                                                                      #
#                                                                             #
# Runs the weighted ensemble TEST simulation. Make sure you ran init.sh first!#
#                                                                             #
###############################################################################

############################### GENERAL SETUP ################################# 

# Set shell option to print commands and their arguments as they are executed.
set -x

# Make sure environment is set else exit
cd $SLURM_SUBMIT_DIR
source env.sh || exit 1

# Print out a sorted list of all the environmental variables
env | sort

############################## ZMQ Work Manager ################################

cd $WEST_SIM_ROOT

SERVER_INFO=$WEST_SIM_ROOT/west_zmq_info-$SLURM_JOBID.json

# Start the ZMQ server : Testing ....
$WEST_ROOT/bin/w_run \
    --work-manager=zmq \
    --n-workers=0 \
    --zmq-mode=master \
    --zmq-write-host-info=$SERVER_INFO \
    --zmq-comm-mode=tcp \
    &> ${LOGDIR}/west-$SLURM_JOBID.log &

# Wait on ZMQ server info file up to one minute
for ((n=0; n<60; n++)); do
  if [ -e $SERVER_INFO ] ; then
    echo "Server info file detected: $SERVER_INFO"
    cat $SERVER_INFO
    break
  fi
  sleep 1
done

# Exit if ZMQ server info file doesn't appear in one minute
if ! [ -e $SERVER_INFO ] ; then
  echo 'Server failed to start'
  exit 1
fi

# Start clients, with the proper number of cores on each :
for node in $(scontrol show hostname $SLURM_NODELIST); do
    ssh -o StrictHostKeyChecking=no $node $PWD/node.sh \
        $SLURM_SUBMIT_DIR $SLURM_JOBID $node \
        --work-manager=zmq \
        --n-workers=24 \
        --zmq-mode=client \
        --zmq-read-host-info=$SERVER_INFO \
        --zmq-comm-mode=tcp &
done

wait 

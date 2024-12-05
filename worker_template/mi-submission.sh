#!/bin/bash

set -euo pipefail

trap 'date "+%Y-%d-%m %T" | tr -d "\n" ; echo "::Exiting $0"' EXIT

# Write date on onset
date "+%Y-%d-%m %T" | tr -d "\n" ; echo "::Entering $0"


export CHASTE_TEST_OUTPUT=/mi/share/scratch/fann/chaste-output

# Chaste Simulation
# Compute simulation number

while :
do
    echo -e "\n\nWaiting for job..."
    tmp="$(python3 -u get_job.py $1)"
    if [[ -z "$tmp" ]]; then
        echo "Exiting with no job found"
        break
    fi


    job_id="$(echo "$tmp" | head -1)"
    name="$(echo "$tmp" | head -2 | tail -n 1)"
    simulation_id="$(echo "$tmp" | head -3 | tail -n 1)"
    args="$(echo "$tmp" | tail -n 1)"
    echo -e "Found job: "
    echo "job_id = $job_id"
    echo "name = $name"
    echo "simulation_id = $simulation_id"
    echo "args = $args"
    echo "handler_id = $1"

    date "+%Y-%d-%m %T" 
    echo -e "\n\n\nRunning CHASTE simulation..."
    /mi/share/scratch/fann/lib/projects/TCellABM/apps/RunTumourEllipticOxygenSimulation \
        $args

    echo -e "\nChaste simulation completed successfully"

    python3 -u finished_job.py $job_id
    date "+%Y-%d-%m %T"
done

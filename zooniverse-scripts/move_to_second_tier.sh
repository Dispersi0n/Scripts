#!/bin/bash -l
#PBS -l walltime=24:00:00,pmem=50mb,nodes=1:ppn=1
#PBS -m abe
#PBS -M kosmala@umn.edu


s3cmd.sh sync /home/packerc/shared/S1 s3://snapshotserengeti 

# Wait for all background processes to finish
wait

#!/bin/sh
#PBS -l walltime=4:00:00,pmem=50mb,nodes=1:ppn=1
#PBS -m abe
#PBS -M kosmala@umn.edu

pbsdsh mysql --host=mysql.msi.umn.edu --user=kosmala --password=uvNaui5sg 
packerc_snapshot_serengeti < 
/home/packerc/shared/metadata_db/scripts/get_all_zooniverse_classifications_S1.sql 
> /home/packerc/shared/metadata_db/scripts/S1_class.tab &

# Wait for all background processes to finish
wait

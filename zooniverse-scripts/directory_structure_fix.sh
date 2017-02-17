# Renames SnapshotSerengeti Directories according to the following pathway:
#
# .../SEASON/SITE/SITE_ROLL/images
# e.g. .../S03/B09/B09_R4/images.jpg
#
############################################################################
#!/bin/sh

directory=$1
output_dir=$2
set -e


####################################################################

### SANITY CHECK ###

USAGE="filerename.sh <input_directory> <output_directory> [S1, S2, ...]"

if test ! -d $directory
then
	echo "Input directory $directory does not exist"
	echo $USAGE
	exit 1
fi

if test ! -d $output_dir
then
	mkdir $output_dir
fi

if [ $# -lt 3 ]
then
	echo "You must specify at least one directory to process"
	echo $USAGE
	exit 1
fi

index=1
for arg in ${@: 1}
do
	if [ $index -gt 2 ]
	then
		if test ! -d $directory/$arg
		then
			echo "Specified directory $directory/$arg does not exist"
			echo $USAGE
			exit 1
		fi
	fi
	index=$(expr $index + 1)
done
	

####################################################################

### MAIN PROGRAM ###

index=1

for season in ${@: 1}
do
	# Skip to season entries after directory and output
	if [ $index -gt 2 ]
	then
		# If season directory does not currently exist in output, then make it
		if test ! -d $output_dir/$season
		then
			mkdir $output_dir/$season
		fi
		for roll in $directory/$season/*
		do
			# Only process directories in $directory/$season
			if test -d $roll
			then
				name=$(basename $roll)
				
				# Change name to all uppercase
				newname=$(echo $name | tr '[:lower:]' '[:upper:]')
				
				# Separate site and roll number
				site=$(echo $newname | cut -d_ -f1 )
				
				# Make season/site directory if does not exist
				if test ! -d $output_dir/$season/$site
				then
					mkdir $output_dir/$season/$site
				fi
				
				# Make season/site/site_roll directory if does not exist
				if test ! -d $output_dir/$season/$site/$newname
				then
				mkdir $output_dir/$season/$site/$newname
				fi
				
				# Cycle through image files in roll
				current_num=0
				for file in $roll/*
				do
					# If file is not a directory copy to output
					if test ! -d $file
					then
						imagename=$(basename $file)
						number=$(echo $imagename | sed 's/[A-Za-z.]//g')
						
						# Extract current image number and save if largest
						if [ $number -gt $current_num ]
						then
							current_num=$number
						fi
						#rm $output_dir/$season/$site/$newname/$imagename
						mv $file $output_dir/$season/$site/$newname/$season"_"$newname"_"$imagename
					fi
				done
				
				# Move and rename image files in subdirectories
				for subdir in $roll/*
				do
					if test -d $subdir
					then
						for file in $subdir/*
						do
							if test ! -d $file
							then
								imagename=$(basename $file)
								current_num=$(expr $current_num + 1)
								digits=$(expr "${current_num}" : '.*')
								zero_total=$(expr 4 - $digits)
								newnum=$current_num
								if [ $zero_total -gt 0 ]
								then
									i=1
									while [ $i -le $zero_total ]
									do
										newnum="0$newnum"
										i=$(expr $i + 1)
									done
								fi
								newimagename=$(echo $imagename | sed -E "s/[0-9]+/$newnum/")
								mv $file $output_dir/$season/$site/$newname/$season"_"$newname"_"$newimagename
							fi
						done
					fi
				done
			fi
		done
	fi
	index=$(expr $index + 1)
done
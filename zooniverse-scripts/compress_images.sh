#!/usr/bin/env bash

# If no arguments given or the argument "-h" print the usage statement
if [ "$1" == "" ] || [ "$1" == "-h" ]
then
	echo -e "USAGE: compress_images.sh <input_directory> <image_file_extension> <output_directory> <output_csv>"
	exit 1
fi

# Read in arguments. A rather unsophisticated way of doing it but the simplest. #
main_directory=$1
extension=$2
output_directory=$3
output_csv=$4
# Set quality score for compression
quality=19

# Recursively list all files in the main directory of files then search for all files containing our target extension. Store in this variable.
directory_files=`ls -R $main_directory | awk '/:$/&&f{s=$0;f=0}/:$/&&!f{sub(/:$/,"");s=$0;f=1;next}NF&&f{ print s"/"$0 }' | grep "$extension"`
# Make output directory. -p prevents error message if directory already exists.
mkdir -p $output_directory
# Drop "." in extension if it was entered as part of that argument. E.g. ".JPG" -> "JPG". Does nothing if no period.
extension="${extension##*.}"
# Go through each file we found with our extension.
for filename in $directory_files
do
	# Since ls -R only gives file names without paths we need to search for our file to get everything.
	file=`basename $filename`
	# Generate three random integers
	r1=$RANDOM
	r2=$RANDOM
	r3=$RANDOM
	# Store our new file name in $newname.
	newname=$r1"_"$r2"_"$r3".$extension"
	if test -f $output_csv
	then
		if ! `grep -q ",*$filename$" $output_csv`
		then
			# In the unlikely case of redundancy in filenames we check our tsv to see if this filename has been generated before.
			while `grep -q "^$newname,*" $output_csv`
			do
				r1=$RANDOM
				r2=$RANDOM
				r3=$RANDOM
				newname=$r1"_"$r2"_"$r3".$extension"
			done
			convert -quality $quality $filename $output_directory/$newname
			echo -e "$newname,$file,$filename" >> $output_csv
		fi
	else
		# Perform the conversion
		convert -quality $quality $filename $output_directory/$newname
		# Add line with new filename, old filename, and old filename with path to our output tsv file
		echo -e "$newname,$file,$filename" >> $output_csv
	fi
done
#!/usr/bin/env bash

dir=$1

mkdir $dir/tmp
index=1
for file in $dir/`ls -tr *.JPG`
do
	file_num=`printf "%04d" $index`
	mv $file $dir/tmp/IMAG$file_num.JPG
	let index=$index+1
done

mv $dir/tmp/* $dir/
rm -rf $dir/tmp 		
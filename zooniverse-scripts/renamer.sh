dir=$1
current_num=0 #Needs to be first number minus 1

for file in $dir/*
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
		mv $file $dir/$newimagename
	fi
done
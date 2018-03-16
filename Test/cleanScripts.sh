#! /bin/bash

cd ../Impact/
shopt -s globstar
sh_files=**/*.sh
for file in $sh_files;
    do
        echo "Modifying file $file. Removing carriage returns and execution privileges"
        tmp_file="$aaaa{file}" 
        tr -d "\r" < $file > $tmp_file 
        rm $file #remove the original file
        mv $tmp_file $file 
	chmod a+x $file 
    done

#!/bin/bash

metric=$1

# extract data between "###" and "div"
sed -n '/^###/,${p;/^div/q}' $1 > temp1

# split the data into focus-areas files based on deliminator </div>
csplit --digits=3 --prefix=outfile temp1 "/<\/div>/+1" "{*}"

# remove both the files
rm $1 temp1

# delete empty files
find . -size 0 -delete

# traverse over output files and rename them
for f in outfile* 
do
	sed -i 's/###/##/' ${f}
	mv ${f} $(grep \#\# ${f} | cut -d - -f 2 | xargs | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g').md

done



## Explanation of above command
#
# grep \#\# ${f}	: to get the line with focus-area name
# cut -d - -f 2		: cut it at deliminator as - and pick the 2nd part
# xargs			: remove starting and trailing whitespace
# tr '[:upper:]' '[:lower:]' : to make it lower case
# sed 's/ /-/g'		: to replace white space with -
# .md			: rename it as focus-area.md file



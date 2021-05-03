#!/bin/bash

metric=$1
link=$2

echo "Downloading $1 from chaoss/website repo..."

wget -q $2

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

	# append the file with gfm version of html tables, via pandoc
	# PS - extract only the table version, else it messes with headings, etc.
	sed -n '/^<table>/,${p;/^<\/table>/q}' ${f} | pandoc --from html --to gfm >> ${f}

	# remove the html table part
	sed -i '/<div>/,/<\/div>/d' ${f}

	# remove hyperlinks
	sed -i 's/[][]\|([^()]*)//g' ${f}

	# rename it with focus-area name
	mv ${f} $(grep \#\# ${f} | cut -d - -f 2 | xargs | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g').md

done

## Explanation of above command
#
# grep \#\# ${f}	: to get the line with focus-area name
# cut -d - -f 2		: cut it at deliminator as - and pick the 2nd part
# xargs				: remove starting and trailing whitespace
# tr '[:lower:]' 	: to make it lower case
# sed 's/ /-/g'		: to replace white space with -
# .md				: rename it as focus-area.md file
#!/bin/bash 

jsonFile='.json'
jsonEmpty='{}'
projectName=$1
fileName='./Data/'$1'_bloated_variants.txt'
echo $fileName

cat $fileName | while read rows
do
echo $rows
if [ ${rows:0-5} = ${jsonFile} ]
# then rm -rf $rows
then echo $jsonEmpty > $rows
else node remove-functions.js $projectName $rows
fi

done

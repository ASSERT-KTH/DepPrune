#!/bin/bash 

jsonFile='.json'
fileName=$1
jsonName=$2
cat $fileName | while read rows
do
echo $rows
if [ ${rows:0-5} = ${jsonFile} ]
# then rm -rf $rows
then cat /dev/null > $rows
else node remove-functions.js $rows $jsonName
fi
#
done

#!/bin/bash 

projectName=$1

fileName='./Playground/'$projectName'/total-files.txt'

projFile=0
depFile=0

nodeStr="/node_modules"

while read rows
do
    echo $rows
    if [[ $rows == *$nodeStr* ]]
    then
        ((depFile++))
    else
        ((projFile++))
    fi
    node function_counter.js $rows $projectName
done < $fileName

echo $projFile
echo $depFile

str=$projectName","$projFile","$depFile
echo $str >> top_total_file_number.txt
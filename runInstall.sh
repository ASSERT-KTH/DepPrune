#!/bin/bash

variantsNum=`cd Variants/yeoman-generator && ls -l |grep "^d"|wc -l`

cd Variants/yeoman-generator

echo $variantsNum

for (( i=$variantsNum; i>=1; i--))
do
    cd variant$i"/yeoman-generator"
    echo `pwd`
    echo "npm install variant"$i
    npm install
    cd ../..
done

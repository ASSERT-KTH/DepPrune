#!/bin/bash
projectName=$1

variantsNum=`cd Variants/$projectName && ls -l |grep "^d"|wc -l`
cd Variants/$projectName

echo $variantsNum

for (( i=$variantsNum; i>=1; i--))
do
    # mkdir variant$i
    cd variant$i/$projectName
    # git clone https://github.com/fastify/fastify.git
    # cd variant$i"/fastify"
    # git checkout 95f9fa5abc105397a715fc376c3a6e704181d2e1
    echo "remove node_modules and install again"
    rm -rf node_modules
    echo "remove done"
    # echo `pwd`
    echo "npm install variant"$i
    npm install
    cd ../..
done

cd ../..


variantsDepsNum=`cd VariantsDeps/$projectName && ls -l |grep "^d"|wc -l`
cd VariantsDeps/$projectName

echo $variantsDepsNum

for (( i=$variantsDepsNum; i>=1; i--))
do
    cd variant$i/$projectName
    echo "remove node_modules and install again"
    rm -rf node_modules
    echo "remove done"
    echo "npm install variant"$i
    npm install
    cd ../..
done

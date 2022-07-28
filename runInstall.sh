#!/bin/bash

variantsNum=`cd VariantsDeps/fastify && ls -l |grep "^d"|wc -l`

cd VariantsDeps/fastify

echo $variantsNum

for (( i=$variantsNum; i>=1; i--))
do
    cd variant$i"/fastify"
    echo `pwd`
    echo "npm install variant"$i
    npm install
    cd ../..
done

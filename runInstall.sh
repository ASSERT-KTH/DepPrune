#!/bin/bash

# variantsNum=`cd VariantsDeps/fastify && ls -l |grep "^d"|wc -l`
variantsNum=14

cd VariantsDeps/fastify

echo $variantsNum

for (( i=$variantsNum; i>=1; i--))
do
    mkdir variant$i
    cd variant$i
    git clone https://github.com/fastify/fastify.git
    # cd variant$i"/fastify"
    cd fastify
    git checkout 95f9fa5abc105397a715fc376c3a6e704181d2e1
    echo `pwd`
    echo "npm install variant"$i
    npm install
    cd ../..
done

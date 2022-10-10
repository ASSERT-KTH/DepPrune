#!/bin/bash
projectName=$1

variantsNum=`cd VariantsFile/$projectName && ls -l |grep "^d"|wc -l`
# variantsNum=44
cd VariantsFile/$projectName

echo $variantsNum

for (( i=$variantsNum; i>=1; i--))
do
    # mkdir variant$i
    cd variant$i
    # git clone https://github.com/yeoman/generator.git
    cd yeoman-generator
    git checkout 8c3e594be57fb866bbccfcc5756475a5b0f853e7
    # echo "remove node_modules and install again"
    # rm -rf node_modules
    # echo "remove done"
    # echo `pwd`
    echo "npm install variant"$i
    npm install
    cd ../..
done

# cd ../..


# variantsDepsNum=`cd VariantsDeps/$projectName && ls -l |grep "^d"|wc -l`
# cd VariantsDeps/$projectName

# echo $variantsDepsNum

# for (( i=$variantsDepsNum; i>=1; i--))
# do
#     cd variant$i/$projectName
#     echo "remove node_modules and install again"
#     rm -rf node_modules
#     echo "remove done"
#     echo "npm install variant"$i
#     npm install
#     cd ../..
# done

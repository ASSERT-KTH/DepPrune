variantPath=$1

variantsNum=`cd $variantPath && ls -l |grep "^d"|wc -l`

echo $variantsNum

for (( i=$variantsNum; i>=1; i--))
do
    cd $variantPath"/variant_"$i
    npm run test
    cd ../../..
done
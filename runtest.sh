projectName=$1

variantsNum=`cd Variants/$projectName && ls -l |grep "^d"|wc -l`

echo $variantsNum
echo $variantsNum > /dev/stderr

for (( i=$variantsNum; i>=1; i--))
do
    cd "./Variants/"$projectName"/variant"$i"/"$projectName
    npm run test
    cd ../../../..
done
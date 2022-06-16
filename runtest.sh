projectName=$1

variantsNum=`cd Variants/$projectName && ls -l |grep "^d"|wc -l`

echo $variantsNum
echo $variantsNum > /dev/stderr

for (( i=$variantsNum; i>=1; i--))
do
    echo "./Variants/"$projectName"/variant"$i"/"$projectName
    cd "./Variants/"$projectName"/variant"$i"/"$projectName
    timeout -k 10s 2m npm run test
    cd ../../../..
done

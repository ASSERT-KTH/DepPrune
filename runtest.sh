projectName=$1
modeName=$2

variantsNum=`cd $modeName/$projectName && ls -l |grep "^d"|wc -l`
# variantsNum=44
echo $variantsNum
echo $variantsNum > /dev/stderr

for (( i=$variantsNum; i>=1; i--))
do
    echo "./"$modeName"/"$projectName"/variant"$i"/"$projectName
    cd "./"$modeName"/"$projectName"/variant"$i"/"$projectName
    timeout -k 10s 2m npm run test
    cd ../../../..
done

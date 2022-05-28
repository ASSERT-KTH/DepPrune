projectName=$1

variantsNum=`cd Variants && ls -l |grep "^d"|wc -l`

echo $variantsNum

for (( i=$variantsNum; i>=1; i--))
do
    cd "./Variants/variant"$i"/"$projectName
    npm run test
    cd ../../..
done
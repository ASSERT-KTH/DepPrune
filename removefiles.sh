projectName=$1
strategyName=$2
filesName='./Data/'$projectName'/'$projectName'_bloated_'$strategyName'_variants.txt'

cat $filesName | while read rows
do
echo $rows
cat /dev/null > $rows
done

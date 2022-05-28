fileName=$1
jsonName=$2
cat $fileName | while read rows
do
echo $rows
cat /dev/null > $rows
done
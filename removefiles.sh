projectName=$1
filesName='./Data/'$projectName'/'$projectName'_file_removal.txt'

cat $filesName | while read rows
do
echo $rows
cat /dev/null > $rows
done

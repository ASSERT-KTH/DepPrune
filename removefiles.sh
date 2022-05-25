jsonFile='.json'
fileName=$1
cat $fileName | while read rows
do
echo $rows
if [ ${rows:0-5} = ${jsonFile} ]
then rm -rf $rows
else node remove-functions.js $rows
fi
# 
done
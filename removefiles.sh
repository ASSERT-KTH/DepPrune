projectName=$1
filesName='./Data/'$projectName'_bloated_variants.txt'
filesNameDeps='./Data/'$projectName'_bloated_deps_variants.txt'

cat $filesName | while read rows
do
echo $rows
cat /dev/null > $rows
done



# cat $filesNameDeps | while read rows
# do
# echo $rows
# cat /dev/null > $rows
# done

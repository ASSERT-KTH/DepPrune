projectName=$1

# fileName='./Playground/'$projectName'/total-files.txt'

cd TestCollection
cd $projectName

npm list --all --omit=dev > npm_list_output_after.txt
grep -v "deduped" npm_list_output_after.txt > npm_list_filtered_output_debloated.txt
unmet=$(grep -c "UNMET" npm_list_filtered_output_debloated.txt)
temp=$(($(wc -l < npm_list_filtered_output_debloated.txt) - 2))
echo $temp
echo $unmet
result=$(($temp - $unmet))
echo $result
rm -rf npm_list_output_after.txt
cd ../..
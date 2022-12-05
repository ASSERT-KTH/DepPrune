projectName=$1

x=0

# echo "remove direct dep before install"

path='Data/'$projectName'/'$projectName'_dependants_url_100.txt'

cat $path | while read rows
do
echo $rows
x=$(( x+1 ))
mkdir ClientTempDir
cd ClientTempDir
echo "I am client "$x", and I am git cloning...."$rows
echo "I am client "$x", and I am git cloning...."$rows >> /dev/stderr
git clone $rows
dirs=(../ClientTempDir/*/)
cd $dirs
echo `pwd`
echo "I am npm installing Client "$dirs
echo "I am npm installing Client "$dirs >> /dev/stderr
npm install
echo "I am runing test of "$dirs" before uninstall"
echo "I am runing test of "$dirs" before uninstall" >> /dev/stderr
timeout -k 10s 5m npm run test
echo "I am npm uninstalling TARGET PROJECT "$projectName
echo "I am npm uninstalling TARGET PROJECT "$projectName >> /dev/stderr
npm uninstall $projectName
echo "I am runing test of "$dirs" after uninstall"
echo "I am runing test of "$dirs" after uninstall" >> /dev/stderr
timeout -k 10s 5m npm run test
cd ../..
rm -rf ClientTempDir

done
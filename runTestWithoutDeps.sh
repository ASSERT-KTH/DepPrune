dir=$(ls -l Clients/ | awk '/^d/ {print $NF}')
for i in $dir
do
    echo $i
    subdir=$(ls -l Clients/$i/ | awk '/^d/ {print $NF}')
    echo 'subdir: '$subdir
    for j in $subdir
    do
        echo '----------------------client '$j' of '$i'----------------------'
        echo $(pwd)
        echo '----------------------client '$j' of '$i'----------------------' >> /dev/stderr
        cd 'Clients/'$i'/'$j
        # npm install
        echo '----------------------start run test before uninstall----------------------'
        echo '----------------------start run test before uninstall----------------------' >> /dev/stderr
        npm run test
        echo 'npm uninstall'
        echo 'npm uninstall' >> /dev/stderr
        npm uninstall $i
        echo '----------------------start run test after uninstall----------------------'
        echo '----------------------start run test after uninstall----------------------' >> /dev/stderr
        timeout -k 300s 2m npm run test
        echo '----------------------run test done----------------------'
        echo '----------------------run test done----------------------' >> /dev/stderr
        cd ../../..
    done
done


projectName=$1

clientsPath='Data/'$projectName'_dependants.log'

cat $clientsPath | while read rows
do
echo $rows
echo "git"
x=$(( x+1 ))
variantPath='variant'$x'/'$projectName
cd $variantPath
echo "uninstalling the dependency "$rows
npm uninstall $rows
cd ../..
done
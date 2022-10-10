projectName=$1

x=0

# echo "remove direct dep before install"

cd './VariantsPureDep/'$projectName
depsPath='../../Data/'$projectName'/'$projectName'_bloated_pure_deps.txt'

cat $depsPath | while read rows
do
echo $rows
x=$(( x+1 ))
variantPath='variant'$x'/'$projectName
cd $variantPath
echo "uninstalling the dependency "$rows
npm uninstall $rows
cd ../..
done
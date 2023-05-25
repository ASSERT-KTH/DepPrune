projectName=$1

# x=0

# echo "remove direct dep before install"

cd './VariantsPureDep/'$projectName
variantPath='variant_deps/'$projectName
cd $variantPath
depsPath='../../../../Data/'$projectName'/'$projectName'_pure_bloated_deps.txt'

cat $depsPath | while read rows
do
echo $rows
# x=$(( x+1 ))
# variantPath='variant_deps/'$projectName
# cd $variantPath
echo "uninstalling the dependency "$rows
npm uninstall $rows
# cd ../..
done
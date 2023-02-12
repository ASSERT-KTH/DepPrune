path='top_target_untested_not_empty.txt'

cat $path | while read rows
do
    echo "I am package "$rows
    echo "I am package "$rows >> /dev/stderr
    folderPath='VariantsPureDep/'$rows'/variant_functions/'$rows
    cd $folderPath

    echo "************************* function based testing begins **************************"
    echo "************************* function based testing begins **************************" >> /dev/stderr
    npm run test
    echo "************************* function based testing ends **************************"
    echo "************************* function based testing ends **************************" >> /dev/stderr

    cd '../../variant_files/'$rows
    echo "************************* file based testing begins **************************"
    echo "************************* file based testing begins **************************" >> /dev/stderr
    npm run test
    echo "************************* file based testing ends **************************"
    echo "************************* file based testing ends **************************" >> /dev/stderr
    
    cd '../../variant_deps/'$rows
    echo "************************* dep based testing begins **************************"
    echo "************************* dep based testing begins **************************" >> /dev/stderr
    npm run test
    echo "************************* dep based testing ends **************************"
    echo "************************* dep based testing ends **************************" >> /dev/stderr
    cd ../../../..
done
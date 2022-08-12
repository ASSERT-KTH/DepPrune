projectName=$1
clientName=$2

variantsNum=`cd Variants/$projectName && ls -l |grep "^d"|wc -l`
echo $(pwd)

echo $variantsNum
echo $variantsNum > /dev/stderr

# For each variant, we test its client under the corresponding dependency
# 1. Unlink the module(variant)'s name
# 2. Globally unlink the previous variant module
# 3. Enter next variant and link globally, run "sudo npm link"
# 4. Enter the client root path, run "npm link module-name"
# 5. Run test for the client, and log it.

for (( i=$variantsNum; i>=1; i--))
do
    echo $clientName" is testing ./Variants/"$projectName"/variant"$i"/"$projectName
    echo $(pwd)
    cd "Clients/"$projectName"/"$clientName

    # step 1
    echo "************* npm unlink module *************"
    npm unlink --no-save $projectName
    echo "************* npm unlink module done *************"

    # step 2
    echo "************* npm unlink globally *************"
    sudo npm rm --global $projectName
    echo "************* npm unlink globally done *************"

    # step 3
    cd "../../../Variants/"$projectName"/variant"$i"/"$projectName
    echo "************* npm link globally *************"
    sudo npm link
    echo "************* npm link globally done *************"

    # step 4
    cd "../../../../Clients/"$projectName"/"$clientName
    echo "************* npm link module *************"
    npm link $projectName
    echo "************* npm link module done *************"

    # step 5
    echo "************* start run test *************"
    # timeout -k 30s 2m npm run test
    timeout -k 300s 2m npm run test
    cd ../../..
    echo "************* run test done *************"
done

# variantsDepsNum=`cd VariantsDeps/$projectName && ls -l |grep "^d"|wc -l`
# echo "variantsDepsNum: "$variantsDepsNum
# echo $(pwd)

# echo $variantsDepsNum
# echo $variantsDepsNum > /dev/stderr


# for (( i=$variantsDepsNum; i>=1; i--))
# do
#     echo $clientName" is testing ./VariantsDeps/"$projectName"/variant"$i"/"$projectName
    
#     cd "Clients/"$projectName"/"$clientName
#     # step 1
#     echo "************* npm unlink module *************"
#     npm unlink --no-save $projectName
#     echo "************* npm unlink module done *************"

#     # step 2
#     echo "************* npm unlink globally *************"
#     sudo npm rm --global $projectName
#     echo "************* npm unlink module done *************"

#     # step 3
#     cd "../../../VariantsDeps/"$projectName"/variant"$i"/"$projectName
#     echo "************* npm link globally *************"
#     sudo npm link
#     echo "************* npm link globally done *************"

#     # step 4
#     cd "../../../../Clients/"$projectName"/"$clientName
#     echo "************* npm link module *************"
#     npm link $projectName
#     echo "************* npm link module done *************"

#     echo "************* start run test *************"
#     # timeout -k 30s 2m npm run test
#     timeout -k 300s 2m npm run test
#     cd ../../..
#     echo "************* run test done *************"
# done

# dirs=(./Data/*/)
# echo $dirs
# cd $dirs
# echo `pwd`


# # Shell to get git url by package name.
# path='top3000_new.txt'
# cat $path | while read rows
# do
# echo $rows
# node get-package-github-url.js $rows
# done

# Shell to git clone and npm install
# path='top43_url.txt'
# cat $path | while read rows
# do
# array=(${rows//,/ })
# package=${array[0]}
# url=${array[1]}

# cd Original
# git clone $url
# cd $package
# npm install
# cyclonedx-npm --output-format JSON --output-file npmlist.json
# nyc npm run test > top43_nyc.log
# #empty devDependencies
# # npm install
# # cyclonedx-npm --output-format JSON --output-file npmlist_runtime.json
# cd ../..
# folderPath='Original/'$package
# echo $folderPath
# # node parseDependencies.js $folderPath
# done


# Shell to git clone and parse package.json
# 1. fetch package name
# 2. collect git url
# 2.1 remove duplicated url (packages)
# 3. revise package name (folder name)
# 4. git clone and parse package.json
# 5. record production packages and development packages from the package.jsons
path='top100_folder.txt'
cat $path | while read rows
do
    echo $rows
    cd Original
    array=(${rows//,/ })
    folder=${array[0]}
    url=${array[1]}
    git clone $url
    cd $folder
    commitID=$(git rev-parse --short HEAD 2>&1)
    str=$folder","$url","$commitID
    echo $str >> ../../top100_commit.txt
    npm install
    # timeout -k 10s 5m nyc npm run test >> ../../originalTests.log
    npm list --json --prod --depth=10 >> ../../productionDependencies.txt
    cd ../..
    python3 parseJson.py $folder
done

# sh testClients.sh deep-equal
# sh testClients.sh execa
# sh testClients.sh express
# sh testClients.sh fastify
# sh testClients.sh finalhandler
# sh testClients.sh levelup
# sh testClients.sh memdown
# sh testClients.sh send
# sh testClients.sh serve-index
# sh testClients.sh session
# sh testClients.sh sharp
# sh testClients.sh meow
# sh testClients.sh yeoman-generator

# dirs=(./Data/*/)
# echo $dirs
# cd $dirs
# echo `pwd`


# Shell to get git url by package name.
# path='top100_runtime.txt'
# cat $path | while read rows
# do
# echo $rows
# node get-package-github-url.js $rows
# done

# Shell to git clone and npm install
path='top43_url.txt'
cat $path | while read rows
do
array=(${rows//,/ })
package=${array[0]}
url=${array[1]}

cd Original
git clone $url
cd $package
npm install
cyclonedx-npm --output-format JSON --output-file npmlist.json
nyc npm run test > top43_nyc.log
#empty devDependencies
# npm install
# cyclonedx-npm --output-format JSON --output-file npmlist_runtime.json
cd ../..
folderPath='Original/'$package
echo $folderPath
# node parseDependencies.js $folderPath
done


# Shell to git clone and parse package.json
# 1. fetch package name
# 2. collect git url
# 3. revise package name (folder name)
# 4. git clone and parse package.json
# 5. record production packages and development packages from the package.jsons
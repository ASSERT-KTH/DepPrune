git clone https://github.com/isaacs/node-glob.git Playground/node-glob

./resetProject.sh Playground/node-glob

python3 genDepList.py Playground/node-glob/ "npm install "

python3 genNycRc.py Playground/node-glob Playground/node-glob/dep_list.txt

cd Playground/node-glob

nyc npm run test 
cd ../..

./transform.sh Playground/node-glob "dynamic" false


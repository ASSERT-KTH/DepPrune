git clone https://github.com/expressjs/compression.git Playground/compression

./resetProject.sh Playground/compression

python3 genDepList.py Playground/compression/ "npm install "

python3 genNycRc.py Playground/compression Playground/compression/dep_list.txt

cd Playground/compression

nyc npm run test 
cd ../..

./transform.sh Playground/compression "dynamic" false


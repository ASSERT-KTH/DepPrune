git clone https://github.com/expressjs/serve-favicon.git Playground/serve-favicon

./resetProject.sh Playground/serve-favicon

python3 genDepList.py Playground/serve-favicon/ "npm install "

python3 genNycRc.py Playground/serve-favicon Playground/serve-favicon/dep_list.txt

cd Playground/serve-favicon

nyc npm run test 
cd ../..

./transform.sh Playground/serve-favicon "dynamic" false


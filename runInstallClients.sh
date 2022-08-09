projectName=$1

# body-parser
clientNames=("express" "skipper" "json-server" "loopback" "routing-controllers")
gitUrls=("https://github.com/expressjs/express.git" "https://github.com/sailshq/skipper.git" "https://github.com/typicode/json-server.git" "https://github.com/strongloop/loopback.git" "https://github.com/typestack/routing-controllers.git")

# send
# clientNames=("serve-static" "restify" "gulp-connect" "fastify-static" "connect-gzip-static")
# gitUrls=("https://github.com/expressjs/serve-static.git" "https://github.com/restify/node-restify.git" "https://github.com/avevlad/gulp-connect.git" "https://github.com/fastify/fastify-static.git" "https://github.com/pirxpilot/connect-gzip-static.git")

# levelup
# clientNames=("pouchdb" "subleveldown" "packager" "dynalite" "multileveldown")
# gitUrls=("https://github.com/pouchdb/pouchdb.git" "https://github.com/Level/subleveldown.git" "https://github.com/Level/packager.git" "https://github.com/mhart/dynalite.git" "https://github.com/Level/multileveldown.git")


for (( i=4; i>=0; i--))
do
    cd Clients/$projectName
    git clone ${gitUrls[$i]}
    cd ${clientNames[$i]}
    npm i
    cd ..
done
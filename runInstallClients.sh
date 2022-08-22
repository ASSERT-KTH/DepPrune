projectName=$1

# body-parser
# clientNames=("express" "skipper" "json-server" "loopback" "routing-controllers")
# gitUrls=("https://github.com/expressjs/express.git" "https://github.com/sailshq/skipper.git" "https://github.com/typicode/json-server.git" "https://github.com/strongloop/loopback.git" "https://github.com/typestack/routing-controllers.git")

# send
# clientNames=("serve-static" "restify" "gulp-connect" "fastify-static" "connect-gzip-static")
# gitUrls=("https://github.com/expressjs/serve-static.git" "https://github.com/restify/node-restify.git" "https://github.com/avevlad/gulp-connect.git" "https://github.com/fastify/fastify-static.git" "https://github.com/pirxpilot/connect-gzip-static.git")

# levelup
# clientNames=("pouchdb" "subleveldown" "packager" "dynalite" "multileveldown")
# gitUrls=("https://github.com/pouchdb/pouchdb.git" "https://github.com/Level/subleveldown.git" "https://github.com/Level/packager.git" "https://github.com/mhart/dynalite.git" "https://github.com/Level/multileveldown.git")

# execa
# clientNames=("username" "lint-staged" "fkill" "semantic-release" "pretty-quick")
# gitUrls=("https://github.com/sindresorhus/username.git" "https://github.com/okonet/lint-staged.git" "https://github.com/sindresorhus/fkill.git" "https://github.com/semantic-release/semantic-release.git" "https://github.com/azz/pretty-quick.git")

# serve-index
# clientNames=("grunt-contrib-connect" "live-server" "server" "fluid-express" "servez-lib")
# gitUrls=("https://github.com/gruntjs/grunt-contrib-connect.git" "https://github.com/tapio/live-server.git" "https://github.com/franciscop/server.git" "https://github.com/fluid-project/fluid-express.git" "https://github.com/greggman/servez-lib.git")

# fastify
# clientNames=("fastify-micro" "fastify-helpers" "tydb" "fastify-vhost" "pubsub-http-handler")
# gitUrls=("https://github.com/47ng/fastify-micro.git" "https://github.com/samurayii/fastify-helpers.git" "https://github.com/alexcorvi/tydb.git" "https://github.com/patrickpissurno/fastify-vhost.git" "https://github.com/cobraz/pubsub-http-handler.git")

# yeoman-generator
# clientNames=("sfdx-plugin-generate" "generator-nuxeo" "generator-tabris-js" "generator-cxcloud" "generator-py")
# gitUrls=("https://github.com/forcedotcom/sfdx-plugin-generate.git" "https://github.com/nuxeo/generator-nuxeo.git" "https://github.com/eclipsesource/generator-tabris-js.git" "https://github.com/cxcloud/generator-cxcloud.git" "https://github.com/kaelzhang/generator-py.git")

# memdown
# clientNames=("pouchdb" "mem" "dynalite" "level-test" "pico-framework")
# gitUrls=("https://github.com/pouchdb/pouchdb.git" "https://github.com/Level/mem.git" "https://github.com/mhart/dynalite.git" "https://github.com/Level/level-test.git" "https://github.com/Picolab/pico-framework.git")

# express-session
# clientNames=("routing-controllers" "server" "Lien" "kraken-js" "kettle")
# gitUrls=("https://github.com/typestack/routing-controllers.git" "https://github.com/franciscop/server.git" "https://github.com/LienJS/Lien.git" "https://github.com/krakenjs/kraken-js.git" "https://github.com/fluid-project/kettle.git")


# compression
clientNames=("hexo-server" "koop-core" "kraken-js" "molstar" "router")
gitUrls=("https://github.com/hexojs/hexo-server.git" "https://github.com/koopjs/koop-core.git" "https://github.com/krakenjs/kraken-js.git" "https://github.com/molstar/molstar.git" "https://github.com/nxus/router.git")


cd Clients/$projectName

for (( i=4; i>=0; i--))
do
    git clone ${gitUrls[$i]}
    cd ${clientNames[$i]}
    npm i
    cd ..
done
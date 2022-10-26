for folder in Original/*
do
    cd $folder
    echo $folder
    # nyc npm run test
    

    # cyclonedx-npm --omit dev --output-file newbom.json

    node ../../parseDependencies.js $folder

    cd ../..

    # const fs = require('fs');

    # let rawdata = fs.readFileSync('sharp/newbom.json')

    # let rawObj = JSON.parse(rawdata)

    # const dependencies = rawObj.dependencies
    # console.log(dependencies.length)
done

const fs = require('fs')
const axios = require('axios')
const acorn = require('acorn')
const walk = require('acorn-walk')

const args = process.argv.slice(2)
const repo = args[0]
const fileUrl = args[1]

// const fileUrl = 'https://raw.githubusercontent.com/eea/volto-datablocks/master/src/index.js' // URL of the JavaScript file
// const fileUrl = 'https://raw.githubusercontent.com/krakenjs/adaro/master/index.js'

axios.get(fileUrl)
    .then(response => {
        const fileContents = response.data;

        // Do something with the file contents
        const ast = acorn.parse(fileContents, {
            ranges: true,
            locations: true,
            sourceType: 'module',
            ecmaVersion: 2020
        })
        walk.full(
            ast,
            /**
             * @param {}
             */
            (node) => {
                // console.log(node)
                if (node.type === 'ImportDeclaration') {
                    console.log('es6')
                    fs.appendFileSync("./Logs/repo_module_system.txt", `${repo}, ES6\n`)
                }
                if (node.type === 'CallExpression' && node.callee.name == 'require') {
                    fs.appendFileSync("./Logs/repo_module_system.txt", `${repo}, CommonJS\n`)
                }
            }
        )
    })
    .catch(error => {
        console.error('Error fetching file:', error);
    });

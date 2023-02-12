const fs = require('fs')
const acorn = require('acorn');
const walk = require('acorn-walk')

const args = process.argv.slice(2)
const folderPath = args[0]
const projectName = args[1]

const sourceFileString = fs.readFileSync(folderPath)
const ast = acorn.parse(sourceFileString, {
    ranges: true,
    locations: true,
    sourceType: 'module',
    ecmaVersion: 2020
})


const fileNameArr = folderPath.split('/')
const nmIndex = fileNameArr.indexOf('node_modules')
const depIndex = nmIndex + 1
const depFileName = fileNameArr.slice(depIndex).join('/')

walk.full(
    ast,
    /**
     * @param {}
     */
    (node) => {
        // console.log(node)
        if (node.type === 'FunctionExpression') {
            countFunc(node, 'FunctionExpression')
        }
        if (node.type === 'ArrowFunctionExpression') {
            countFunc(node, 'ArrowFunctionExpression')
        }
        if (node.type === 'FunctionDeclaration') {
            countFunc(node, 'FunctionDeclaration')
        }
    }
)

function countFunc(node, type) {
    const funcName = node.loc ? `${type}, ${depFileName}_function_${JSON.stringify(node.loc.start)}` : `${type}, function_in_class`
    console.log(`${funcName} has been counted`)
    if (nmIndex > -1) {
        fs.appendFileSync(`./Data/${projectName}/${projectName}_deps_total_functions.txt`, `${funcName}` + '\n')
    } else {
        fs.appendFileSync(`./Data/${projectName}/${projectName}_proj_total_functions.txt`, `${funcName}` + '\n')
    }
}
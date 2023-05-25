const Walker = require('node-source-walk')
const recast = require('recast')
const types = require('ast-module-types')
const fs = require('fs')

const args = process.argv.slice(2)
const folderPath = args[0]

const sourceFileString = fs.readFileSync(folderPath)
const ast = recast.parse(sourceFileString)
const walker = new Walker()

const dependencies = [];

walker.walk(ast, (node) => {
    // console.log(ast)
    // console.log(node)
    if (!types.isRequire(node) || !node.arguments || node.arguments.length === 0) {
        return
    }

    if (types.isPlainRequire(node)) {
        const result = extractDependencyFromRequire(node)
        if (result) {
            dependencies.push(result)
        }
    } else if (types.isMainScopedRequire(node)) {
        dependencies.push(extractDependencyFromMainRequire(node))
    }
})

console.log(dependencies)

function extractDependencyFromRequire(node) {
    if (node.arguments[0].type === 'Literal' || node.arguments[0].type === 'StringLiteral') {
      return node.arguments[0].value;
    }
  
    if (node.arguments[0].type === 'TemplateLiteral') {
      return node.arguments[0].quasis[0].value.raw;
    }
  }
  
  function extractDependencyFromMainRequire(node) {
    return node.arguments[0].value;
  }
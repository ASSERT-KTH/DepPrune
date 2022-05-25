const recast = require('recast')
const fs = require('fs')

const args = process.argv.slice(2)
const folderPath = args[0]
const depName = args[1]

const sourceFileString = fs.readFileSync(folderPath)
const ast = recast.parse(sourceFileString)
const astBody = ast.program.body

// console.log(astBody)

function getRequire(node, index) {
    recast.visit(node, {
        visitExpressionStatement: function ({ value }) {
            if (value.expression.right && value.expression.right.type && value.expression.right.type === 'CallExpression') {
                if (value.expression.right.callee && value.expression.right.callee.name === 'require') {
                    console.log(value.expression.right.arguments[0].value)
                    if (value.expression.right.arguments[0].value === depName)
                    astBody.splice(index, 1)
                }
            }
            console.log(111, value.type)
            getRequire(value.expression)
            
            return false
        },
        VariableDeclaration: function ({ value }) {
            console.log(333, value.type)
            if (value.declarations && value.declarations[0].init && value.declarations[0].init.type === 'CallExpression') {
                console.log(value.declarations)
            }
            return false
        }
        
    })
}
for (let i = 0; i < astBody.length; i++) {
    getRequire(astBody[i], i)
}

// const targetFileString = recast.print(ast).code
// fs.writeFileSync(folderPath, targetFileString, 'utf-8')

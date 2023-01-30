const recast = require('recast')
const fs = require('fs')

const args = process.argv.slice(2)
const folderPath = args[0]

const sourceFileString = fs.readFileSync(folderPath)
const ast = recast.parse(sourceFileString)
const astBody = ast.program.body


// filePath example:
// /Users/sandzn/Documents/Develop/multee/Variants/express/variant15/express/node_modules/function-bind/implementation.js
const fileNameArr = folderPath.split('/')
const nmIndex = fileNameArr.indexOf('node_modules')
const depIndex = nmIndex + 1
const depFileName = fileNameArr.slice(depIndex).join('/')

function removeUFF(node) {
    const insertString = `lyx`
    const insertAst = recast.parse(insertString).program.body[0]
    node.body.body = []
    node.body.body.unshift(insertAst)

    const funcName = node.loc ? `${depFileName}_function_${node.loc.start.line}_${node.loc.start.column}` : `${depFileName}_function_in_class`
    console.log(`${funcName} has been removed`)
}

function forRemoveCycle(nodeArr) {
    const len = nodeArr.length
    for (let i = 0; i < len; i++) {
        removeFunctions(nodeArr[i])
    }
}

function removeFunctions(node) {
    recast.visit(node, {
        // 1
        visitFunctionDeclaration: function ({ value }) {
            // console.log('visitFunctionDeclaration', index++)
            removeUFF(value)
            return false
        },
        // 2
        visitFunctionExpression: function ({ value }) {
            // console.log('visitFunctionExpression', index++)
            removeUFF(value)
            return false
        },
        // 3
        visitVariableDeclaration: function ({ value }) {
            // console.log('visitVariableDeclaration', index++)
            forRemoveCycle(value.declarations)
            return false
        },
        // 4
        visitVariableDeclarator: function ({ value }) {
            // console.log('visitVariableDeclarator', index++)
            removeFunctions(value.init)
            return false
        },
        // 5
        visitCallExpression: function ({ value }) {
            // console.log('visitCallExpression', index++)
            removeFunctions(value.callee)
            forRemoveCycle(value.arguments)
            return false
        },
        // 6
        visitReturnStatement: function ({ value }) {
            // console.log('visitReturnStatement', index++)
            removeFunctions(value.argument)
            return false
        },
        // 7
        visitExpressionStatement: function ({ value }) {
            //   console.log('visitExpressionStatement', index++)
            removeFunctions(value.expression)
            return false
        },
        // 8
        visitUnaryExpression: function ({ value }) {
            //   console.log('visitUnaryExpression', index++)
            removeFunctions(value.argument)
            return false
        },
        // 9
        visitSequenceExpression: function ({ value }) {
            //   console.log('visitSequenceExpression', index++)
            forRemoveCycle(value.expressions)
            return false
        },
        // 10
        visitAssignmentExpression: function ({ value }) {
            //   console.log('visitAssignmentExpression', index++)
            removeFunctions(value.right)
            return false
        },
        // 11
        visitConditionalExpression: function ({ value }) {
            //   console.log('visitConditionalExpression', index++)
            removeFunctions(value.test)
            removeFunctions(value.consequent)
            removeFunctions(value.alternate)
            return false
        },
        // 12
        visitLogicalExpression: function ({ value }) {
            //   console.log('visitLogicalExpression', index++)
            removeFunctions(value.left)
            removeFunctions(value.right)
            return false
        },
        // 13
        visitIfStatement: function ({ value }) {
            //   console.log('visitIfStatement', index++)
            removeFunctions(value.consequent)
            removeFunctions(value.alternate)
            return false
        },
        // 14
        visitUnaryExpression: function ({ value }) {
            //   console.log('visitUnaryExpression', index++)
            removeFunctions(value.argument)
            return false
        },

        // 15
        visitArrayExpression: function ({ value }) {
            //   console.log('visitArrayExpression', index++)
            forRemoveCycle(value.elements)
            return false
        },
        // 16
        visitObjectExpression: function ({ value }) {
            //   console.log('visitObjectExpression', index++)
            forRemoveCycle(value.properties)
            return false
        },
        // 17
        visitProperty: function ({ value }) {
            //   console.log('visitProperty', index++)
            removeFunctions(value.value)
            return false
        },
        // 18
        visitForStatement: function ({ value }) {
            //   console.log('visitForStatement', index++)
            removeFunctions(value.init)
            removeFunctions(value.body)
            return false
        },
        // 19
        visitWhileStatement: function ({ value }) {
            //   console.log('visitWhileStatement', index++)
            removeFunctions(value.body)
            return false
        },
        // 20
        visitDoWhileStatement: function ({ value }) {
            //   console.log('visitDoWhileStatement', index++)
            removeFunctions(value.body)
            return false
        },
        // 21
        visitBlockStatement: function ({ value }) {
            //   console.log('visitBlockStatement', index++)
            forRemoveCycle(value.body)
            return false
        },
        // 22
        visitSwitchStatement: function ({ value }) {
            //   console.log('visitSwitchStatement', index++)
            forRemoveCycle(value.cases)
            return false
        },
        // 23
        visitSwitchCase: function ({ value }) {
            //   console.log('visitSwitchCase', index++)
            forRemoveCycle(value.consequent)
            return false
        },
        // 24
        visitThrowStatement: function ({ value }) {
            //   console.log('visitThrowStatement', index++)
            removeFunctions(value.argument)
            return false
        },
        // 25
        visitTryStatement: function ({ value }) {
            //   console.log('visitThrowStatement', index++)
            removeFunctions(value.block)
            removeFunctions(value.handler)
            return false
        },
        // 26
        visitCatchClause: function ({ value }) {
            //   console.log('visitThrowStatement', index++)
            removeFunctions(value.body)
            return false
        },
        visitClassDeclaration: function ({ value }) {
            removeFunctions(value.body)
            return false
        },
        visitClassBody: function ({ value }) {
            forRemoveCycle(value.body)
            return false
        },
        visitMethodDefinition: function ({ value }) {
            removeFunctions(value.value)
            return false
        },
        visitArrowFunctionExpression: function ({ value }) {
            removeUFF(value)
            return false
        }
    })
}



for (let i = 0; i < astBody.length; i++) {
    removeFunctions(astBody[i], i)
}

const targetFileString = recast.print(ast).code
fs.writeFileSync(folderPath, targetFileString, 'utf-8')

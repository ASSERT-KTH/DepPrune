const recast = require('recast')
const fs = require('fs')

const args = process.argv.slice(2)
const folderPath = args[0]
const depName = args[1]


const sourceFileString = fs.readFileSync(folderPath)
const ast = recast.parse(sourceFileString)
const astBody = ast.program.body

function forCycle(nodeArr, astBody, index) {
    const len = nodeArr.length
    if (len === 1) {
        removeRequirement(nodeArr[0], astBody, index, false)
    } else {
        for (let i = 0; i < len; i++) {
            removeRequirement(nodeArr[i], nodeArr, i, true)
        }
    }
}

function isRequirementInCallExpression(node) {
    if (node.type != 'CallExpression') return false
    if (node.callee.type == 'Identifier' &&
        node.callee.name == 'require') {
        return true
    }
    if (node.callee.type == 'CallExpression') {
        isRequirementInCallExpression(node.callee)
        return true
    }
    if (node.callee.type == 'MemberExpression') {
        isRequirementInCallExpression(node.arguments)
        return true
    }
    if (node.arguments[0] && node.arguments[0].type == 'CallExpression') {
        isRequirementInCallExpression(node.arguments[0])
        return true
    }
    return false
}

function mightBeRemoved(node, astBody, astIndex, inFor) {
    recast.visit(node, {
        visitLiteral: function (node) {
            if (node.value.value == depName) {
                console.log(`${depName} is removed from ${folderPath}`)
                if (inFor) {
                    astBody.splice(astIndex, 1)
                } else {
                    const emptyString = ''
                    const insertAst = recast.parse(emptyString).program.body[0]
                    astBody.splice(astIndex, 1, insertAst)
                }
                return true
            }
            return false
        }
    })
}

function removeRequirement(node, astBody, index, inFor) {
    recast.visit(node, {
        visitVariableDeclaration: function ({ value }) {
            // console.log('visitVariableDeclaration')
            forCycle(value.declarations, astBody, index)
            return false
        },
        visitVariableDeclarator: function ({ value }) {
            // console.log('visitVariableDeclarator')
            if (value.init && value.init.type && value.init.type == 'CallExpression') {
                const callNode = value.init
                if (isRequirementInCallExpression(callNode)) {
                    mightBeRemoved(callNode, astBody, index, inFor)
                }
            } if (value.init && value.init.type && value.init.type == 'MemberExpression') {
                const callNode = value.init.object
                if (isRequirementInCallExpression(callNode)) {
                    // console.log('visitMemberExpression')
                    mightBeRemoved(callNode, astBody, index, inFor)
                }
            }
            return false
        },
        visitExpressionStatement: function ({ value }) {
            // console.log('ExpressionStatement')
            if (value.expression.type == 'CallExpression') {
                const callNode = value.expression.callee
                if (isRequirementInCallExpression(callNode)) {
                    mightBeRemoved(callNode, astBody, index)
                }
            }
            if (value.expression.callee && value.expression.callee.type == 'FunctionExpression') {
                // console.log('FunctionExpression')
                funcNodeCallee = value.expression.callee
                removeRequirement(funcNodeCallee)
                funcNodeArg = value.expression.arguments
                removeRequirement(funcNodeArg)
            }
            return false
        },
        visitFunctionExpression: function ({ value }) {
            // console.log('FunctionExpression')
            forCycle(value.body.body)
            return false
        }
    })
}



for (let i = 0; i < astBody.length; i++) {
    removeRequirement(astBody[i], astBody, i)
}

const targetFileString = recast.print(ast).code
fs.writeFileSync(folderPath, targetFileString, 'utf-8')
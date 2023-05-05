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
    return false
}

function mightBeRemoved(node, astBody, astIndex, inFor) {
    recast.visit(node, {
        visitLiteral: function (node) {
            // console.log(node)
            if (node.value.value == depName) {
                console.log(`${depName} is removed from the dependent`)
                if (inFor) {
                    console.log(222)
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
            console.log(value.parent)
            forCycle(value.declarations, astBody, index)
            return false
        },
        visitVariableDeclarator: function ({ value }) {
            // console.log('visitVariableDeclarator', index++)
            if (value.init.type == 'CallExpression') {
                // console.log(value, astBody)
                const callNode = value.init
                if (isRequirementInCallExpression(callNode)) {
                    console.log('visitVariableDeclaration')

                    mightBeRemoved(callNode, astBody, index, inFor)
                }
            } if (value.init.type == 'MemberExpression') {
                const callNode = value.init.object
                if (isRequirementInCallExpression(callNode)) {
                    console.log('visitMemberExpression')
                    mightBeRemoved(callNode, astBody, index, inFor)
                }
            }
            return false
        },
        visitExpressionStatement: function ({ value }) {
            //   console.log('visitExpressionStatement', index++)
            console.log('CallExpression')
            console.log(value.parentPath)
            if (value.expression.type == 'CallExpression') {
                const callNode = value.expression.callee
                console.log('CallExpression')
                if (isRequirementInCallExpression(callNode)) {
                    console.log('CallExpression')
                    mightBeRemoved(callNode, astBody, index)
                }
            }
            return false
        }
    })
}



for (let i = 0; i < astBody.length; i++) {
    removeRequirement(astBody[i], astBody, i)
}

const targetFileString = recast.print(ast).code
fs.writeFileSync(folderPath, targetFileString, 'utf-8')
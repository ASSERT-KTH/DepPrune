const fs = require('fs')

const jsonData = fs.readFileSync('./dependency-tree.json')
const unusedFilesData = fs.readFileSync('./unused-files.txt', 'utf-8')
const dataObj = JSON.parse(jsonData)
const unusedFiles = unusedFilesData.split('\n')

fs.writeFileSync('./wrapped-dependency-tree.json', '')

let unusedNodesSet = []
let tempArr = []
let newSet = []

// let wrappedTree = {}
function visitDepTree(dataObj) {
    let wrappedTree = {}
    for (let key in dataObj) {
        wrappedTree['path'] = key
        wrappedTree['isFlaged'] = false
        wrappedTree['children'] = []
        const value = dataObj[key]
        if (isFileUnused(key)) {
            wrappedTree['isUnused'] = true
        } else {
            wrappedTree['isUnused'] = false
        }
        
        if (isFileALeaf(value)) {
            // leaf
            wrappedTree['isLeaf'] = true
            wrappedTree['isBranch'] = false
            wrappedTree['children'] = []
        } else {
            wrappedTree['isLeaf'] = false
            wrappedTree['isBranch'] = true
            // wrappedTree['children'].push(visitDepTree(value))
            // has dependencies, recursively traverse
            wrappedTree['children'] = turnValueToChildren(value)
            // visitDepTree(value)
        }
    }
    return wrappedTree
}

function turnValueToChildren(value) {
    let children = []
    for (let key in value) {
        isLeaf = isFileALeaf(value[key])
        const child = {
            'path': key,
            'isLeaf': isLeaf,
            'isBranch': !isLeaf,
            'isUnused': isFileUnused(key),
            'isFlaged': false,
            'children': turnValueToChildren(value[key])
        }
        children.push(child)
    }
    return children
}

function isFileUnused(filepath) {
    return unusedFiles.indexOf(filepath) > -1
}

function isFileALeaf(value) {
    return typeof value === 'object' && JSON.stringify(value) == '{}'
}

function isUnusedTree(node) {
    const children = node.children
    let childrenUnused = false

    if (children.length) {
        children.forEach(child => {
          if (isUnusedTree(child)) childrenUnused = true
        })
        return node.isUnused && childrenUnused
    } else {
        return node.isUnused
    }  
}

function logUnusedTree(node) {
    tempArr.push(node.path)
    const children = node.children
    if (children.length) {
        children.forEach(child => {
            logUnusedTree(child)
        })
    }
    // console.log(tempArr)
    unusedNodesSet.push(tempArr)
}


function traverseTree(node) {
    tempArr = []
    if (isUnusedTree(node)) {
        logUnusedTree(node)
        return
    } 
    const children = node.children
    children.forEach(child => {
        traverseTree(child)
    })
}


// Convert dependency-tree to wrapped-tree. For each node in dependency-tree, 
// generate a new node with path, isLeaf, isUnused, isBranch, children
const result = visitDepTree(dataObj)

// fs.writeFileSync('./wrapped-dependency-tree.json', JSON.stringify(result))

traverseTree(result)


unusedNodesSet.forEach(node => {
    str = JSON.stringify(node)
    if (newSet.indexOf(str) == -1) {
        newSet.push(str)
    }
})

console.log(newSet)
// result.children.forEach(item => { 
//     console.log(isUnusedTree(item))
// })
// console.log(isUnused)


// Find subtrees (more of which may be leaves), and generate a set of minimum debloating nodes.


// console.log(result)
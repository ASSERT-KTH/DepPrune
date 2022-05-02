let fs = require('fs')
let dependencyTree = require('dependency-tree')

let tree = dependencyTree({
    filename: 'index.js',
    directory: './'
})

var list = dependencyTree.toList({
    filename: 'index.js',
    directory: './'
  })

let data = JSON.stringify(tree);
fs.writeFileSync('dependency-tree.json', data)

list.forEach(function (file) {
    file += '\n'
    fs.appendFileSync('dependency-tree-list.txt', file)
})

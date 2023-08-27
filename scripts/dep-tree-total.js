const args = process.argv.slice(2)
const folderPath = args[0]
const entryFile = args[1]

let fs = require('fs')
let dependencyTree = require('dependency-tree')
let jsonObj = {}

const totalDepsData = fs.readFileSync(`./${folderPath}/total__deps.txt`, 'utf-8')
const totalDeps = totalDepsData.split('\n')

let tree = dependencyTree({
    filename: `${folderPath}/${entryFile}`,
    directory: `./${folderPath}`
})

// console.log(tree)

function identifyParentFile(dataObj, depName) {
    if (Object.keys(dataObj).length === 0) return
    for (let key in dataObj) {
        children = dataObj[key]
        for (let child in children) {
            if (child.includes(`/node_modules/${depName}/`) && arr.indexOf(key) == -1) {
                arr.push(key)
            }

            identifyParentFile(children, depName)
        }
    }
}
let arr = []
totalDeps.forEach(dep => {
    arr = []
    if (dep == "") return
    depName = dep.split('__')[0]

    identifyParentFile(tree, depName)
    console.log(arr)
    jsonObj[depName] = arr
})

let data = JSON.stringify(jsonObj, null, 2)
fs.writeFileSync(`./${folderPath}/dependent-files-total.json`, data)


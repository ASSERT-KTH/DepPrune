const args = process.argv.slice(2)
const folderPath = args[0]
const projectName = args[1]
const repoUrl = args[2]
const commit = args[3]
const fs = require('fs')

const { spawn } = require("child_process")

fs.writeFileSync(`./Data/${projectName}/${projectName}_bloated_subtree_variants.txt`, '')
const wrappedJsonData = fs.readFileSync(`./${folderPath}/wrapped-dependency-tree.json`)
const dataObj = JSON.parse(wrappedJsonData)
let unusedSubtrees = []
let tempArr = [] // a temporary subtree
let candidates = []
let bloatedJsonList = []

function generateVariant(files, index) {
    // copyProject:
    const variantPath = `VariantsSubtree/${projectName}/variant${index + 1}/${projectName}`
    console.log('start generating ', variantPath)

    const gitCommand = spawn(`git clone ${repoUrl} ${variantPath} && cd ${variantPath} && git checkout ${commit} && npm install && cd ../../.. `, {
        shell: true
    })
    console.log('start generating deps variants', index + 1)
    gitCommand.stdout.on("data", data => {
        console.log(`stdout: ${data}`);
    });

    gitCommand.on('error', (error) => {
        console.log(`error: ${error.message}`);
    });

    gitCommand.on("close", code => {
        console.log(`child process exited with code ${code}`);
    });

    // Change names for files in candidate
    const newfiles = files.map(file => { return file.replace(`${folderPath}`, `${variantPath}`) })
    newfiles.forEach(file => {
        console.log(file)
        const fileStr = file + '\n'
        fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_subtree_variants.txt`, fileStr)
    })
}

function isNodeUnused(node) {
    return node.isUnused || bloatedJsonList.indexOf(node.path) > -1
}

function isUnusedTree(node) {
    const children = node.children
    let childrenUnused = true

    if (children.length) {
        children.forEach(child => {
            if (!isUnusedTree(child)) childrenUnused = false
        })
        return node.isUnused && childrenUnused
    } else {
        // if a leaf is js node: check unused
        // if a leaf is json node: check in bloatedJsonList
        return isNodeUnused(node)
    }
}

function LogNode(node) {
    const path = node.path
    tempArr.push(path)
    const children = node.children
    if (children.length) {
        children.forEach(child => {
            LogNode(child)
        })
    }
    return tempArr
}

function logUnusedTree(node) {
    tempArr = []
    tempArr = LogNode(node)
    unusedSubtrees.push(tempArr)
    return tempArr
}

function logJSON(node) {
    // console.log('json node', node)
    const path = node.path
    const idx = bloatedJsonList.indexOf(path)
    // if JSON's parent is unused, push it to bloatedJsonList. 
    // Otherwise, remove it from bloatedJsonList (if it's already existed in the bloatedJsonList)
    if (idx === -1 && node.isParentUnused) {
        bloatedJsonList.push(path)
    } else if (idx > -1 && !node.isParentUnused) {
        bloatedJsonList.splice(idx, 1)
    }
}

function checkNode(node) {
    // When we visit a node, we make the following two judgements.
    // 1st judgement: If the node is unused, then 2nd judgement:
    // If the subtree with this node as the root has all its nodes unused, then
    // push the subtree to candidates.
    const key = node.path
    if (key && key.slice(-5).toLocaleLowerCase() === '.json') {
        logJSON(node)
    }

    if (node.isUnused) {
        if (isUnusedTree(node)) {
            // If all offsprings are unused files, take this subtree as a candidate
            // don't check its offsprings
            logUnusedTree(node)
            return
        }
    }

    const children = node.children
    if (!children.length) return

    children.forEach(child => {
        checkNode(child)
    })
}

// Calculate the bloated subtrees.
// A bloated subtree means all the nodes on the subtree are bloated.
checkNode(dataObj)

// de-duplicate
unusedSubtrees.forEach(set => {
    str = JSON.stringify(set)
    if (candidates.indexOf(str) == -1) {
        candidates.push(str)
    }
})

console.log(`Candidates in ${projectName}: ${candidates.length} \n\n`)
fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_subtree_candidates.txt`, `Candidates in ${projectName}: ${candidates.length} \n\n`)
candidates.forEach((candidate, index) => {
    const files = JSON.parse(candidate)
    console.log(files)
    fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_subtree_candidates.txt`, candidate + '\n')
    generateVariant(files, index)
})

bloatedJsonList.forEach((json, index) => {
    console.log(json)
    fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_json.txt`, json + '\n')
})
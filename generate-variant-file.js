const args = process.argv.slice(2)
const folderPath = args[0]
const projectName = args[1]
const repoUrl = args[2]
const commit = args[3]
const fs = require('fs')

const { spawn } = require("child_process")
const { json } = require('stream/consumers')

fs.writeFileSync(`./Data/${projectName}/${projectName}_bloated_file_variants.txt`, '')
fs.writeFileSync(`./Data/${projectName}/${projectName}_bloated_file_candidates.txt`, '')
const wrappedJsonData = fs.readFileSync(`./${folderPath}/wrapped-dependency-tree.json`)
const dataObj = JSON.parse(wrappedJsonData)
let bloatedFiles = []
let tempArr = [] // a temporary subtree
let candidates = []
let bloatedJsonList = []
let deDupBloatedSets = [] // sets for js with json

function generateVariant(files, index) {
    // copyProject:
    const variantPath = `VariantsFile/${projectName}/variant${index + 1}/${projectName}`
    console.log('start generating ', variantPath)

    const gitCommand = spawn(`git clone ${repoUrl} ${variantPath} && cd ${variantPath} && git checkout ${commit} && npm install && cd ../../.. `, {
        shell: true
    })
    console.log('start generating files variants', index + 1)
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
        fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_file_variants.txt`, fileStr)
    })
}

function logUnusedFile(node) {
    bloatedFiles.push(node.path)
}

function logJSON(node) {
    // console.log('json node', node)
    const path = node.path
    const parent = node.parent
    const jsonObj = {
        path,
        parent
    }
    const idx = bloatedJsonList.indexOf(jsonObj)
    // if JSON's parent is unused, push it to bloatedJsonList. 
    // Otherwise, remove it from bloatedJsonList (if it's already existed in the bloatedJsonList)
    if (idx === -1 && node.isParentUnused) {
        bloatedJsonList.push(jsonObj)
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
        logUnusedFile(node)
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

console.log('json', bloatedJsonList)

const deDupBloatedFiles = Array.from(new Set(bloatedFiles))
console.log("deDupBloatedFiles", deDupBloatedFiles)

deDupBloatedFiles.forEach(file => {
    tempArr = []
    tempArr.push(file)
    bloatedJsonList.forEach(jsonObj => {
        if (jsonObj.parent === file && tempArr.indexOf(jsonObj.path) === -1) {
            tempArr.push(jsonObj.path)
        }
    })
    deDupBloatedSets.push(tempArr)
})

console.log("deDupBloatedSets", deDupBloatedSets)

// de-duplicate
deDupBloatedSets.forEach(set => {
    str = JSON.stringify(set)
    if (candidates.indexOf(str) == -1) {
        candidates.push(str)
    }
})

console.log(`Candidates in ${projectName}: ${candidates.length} \n\n`)
fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_file_candidates.txt`, `Candidates in ${projectName}: ${candidates.length} \n\n`)
candidates.forEach((candidate, index) => {
    const files = JSON.parse(candidate)
    console.log(files)
    fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_file_candidates.txt`, candidate + '\n')
    generateVariant(files, index)
})

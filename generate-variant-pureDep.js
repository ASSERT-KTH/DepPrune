const args = process.argv.slice(2)
const folderPath = args[0]
const projectName = args[1]
const repoUrl = args[2]
const commit = args[3]
const fs = require('fs')

const { spawn } = require("child_process")

const bloatedPureDepsData = fs.readFileSync(`./Data/${projectName}/${projectName}_bloated_pure_deps.txt`, 'utf-8')
const bloatedNodesData = fs.readFileSync(`./Data/${projectName}/${projectName}_bloated_nodes.txt`, 'utf-8')
fs.writeFileSync(`./Data/${projectName}/${projectName}_bloated_pure_deps_variants.txt`, '')
let bloatedPureDeps = bloatedPureDepsData.split('\n')
bloatedPureDeps.pop()

const bloatedNodes = bloatedNodesData.split('\n')

bloatedPureDeps.forEach((dep, index) => {
    const variantPath = `VariantsPureDep/${projectName}/variant${index + 1}/${projectName}`
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
})

bloatedNodes.forEach(node => {
    const pathArr = node.split("/")
    const nodeMIdx = pathArr.indexOf("node_modules")
    const depName = pathArr[nodeMIdx + 1]
    const variantIndex = bloatedPureDeps.indexOf(depName)
    
    if (variantIndex >= 0) {
        const variantPath = `VariantsPureDep/${projectName}/variant${variantIndex + 1}/${projectName}`

        // Change names for files in each dep
        const newPath = node.replace(`${folderPath}`, `${variantPath}`)
        fs.appendFileSync(`./Data/${projectName}/${projectName}_bloated_pure_deps_variants.txt`, newPath + '\n')
    }
})
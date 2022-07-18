const args = process.argv.slice(2)
const folderPath = args[0]
const projectName = args[1]
const repoUrl = args[2]
const commit = args[3]

const fs = require('fs')
const childProcess = require('child_process')

const bloatedDepsData = fs.readFileSync(`./Data/${projectName}_bloated_deps.txt`, 'utf-8')
const bloatedNodesData = fs.readFileSync(`./Data/${projectName}_bloated_nodes.txt`, 'utf-8')
fs.writeFileSync(`./Data/${projectName}_bloated_deps_variants.txt`, '')

let bloatedDeps = bloatedDepsData.split('\n')
bloatedDeps.pop()

const bloatedNodes = bloatedNodesData.split('\n')

bloatedDeps.forEach((dep, index) => {
    const variantPath = `VariantsDeps/${projectName}/variant${index + 1}/${projectName}`

    console.log('start generating deps variants', index + 1)
    childProcess.exec(`git clone ${repoUrl} ${variantPath} && cd ${variantPath} && git checkout ${commit} && npm install --force && cd ../../.. `,
        (err, stdout, stderr) => {
            if (err) console.log(err)
            console.log(stdout.toString())
        }
    )
})



bloatedNodes.forEach(node => {
    const pathArr = node.split("/")
    const nodeMIdx = pathArr.indexOf("node_modules")
    const depName = pathArr[nodeMIdx + 1]
    const variantIndex = bloatedDeps.indexOf(depName)

    const variantPath = `VariantsDeps/${projectName}/variant${variantIndex + 1}/${projectName}`

    // Change names for files in each dep
    const newPath = node.replace(`${folderPath}`, `${variantPath}`)
    fs.appendFileSync(`./Data/${projectName}_bloated_deps_variants.txt`, newPath + '\n')
})
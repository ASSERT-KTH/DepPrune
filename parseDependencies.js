const args = process.argv.slice(2)
const folderPath = args[0]

const fs = require('fs')

let rawdata = fs.readFileSync(`${folderPath}/newbom.json`)

let rawObj = JSON.parse(rawdata)

const dependencies = rawObj.dependencies
console.log(folderPath)
console.log(dependencies.length - 1)
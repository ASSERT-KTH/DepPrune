const args = process.argv.slice(2)
const packageName = args[0]
console.log(packageName)
const fs = require('fs')

let rawdata = fs.readFileSync(`Original/${packageName}/package.json`)

let rawObj = JSON.parse(rawdata)

const dependencies = rawObj.dependencies
if (dependencies) {
    console.log("dependencies", dependencies)
    const depLen = dependencies.length
    console.log("depLen", depLen)
    fs.appendFileSync(`dependencies.log`, `${packageName},${depLen},${JSON.stringify(dependencies)}` + '\n')
}

const devDependencies = rawObj.devDependencies
if (devDependencies) {
    console.log("devDependencies", devDependencies)
    const devDepLen = devDependencies.length
    console.log("devDepLen", devDepLen)
    fs.appendFileSync(`devDependencies.log`, `${packageName},${devDepLen},${JSON.stringify(devDependencies)}` + '\n')
}
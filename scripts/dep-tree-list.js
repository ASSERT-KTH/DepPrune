const args = process.argv.slice(2)
const folderPath = args[0]
const entryFile = args[1]

let fs = require('fs')
let dependencyTree = require('dependency-tree')

var list = dependencyTree.toList({
    filename: `${folderPath}/${entryFile}`,
    directory: `./${folderPath}`
})

// fs.writeFileSync(folderPath, targetFileString, 'utf-8')
// Path to the file where data will be written
const outputPath = `./${folderPath}/dependency-tree-list.txt`

// Create a writable stream to the output file
const writeStream = fs.createWriteStream(outputPath)

// Loop through the array and write each element to the file
list.forEach((line) => {
  // Write the current line followed by a newline character
  writeStream.write(line + '\n')
});

// Close the write stream when done writing
writeStream.end()

// Listen for the 'finish' event to know when writing is complete
writeStream.on('finish', () => {
  console.log(`Data has been written to the file in ${folderPath}.`)
});

// Handle errors in writing to the file
writeStream.on('error', (error) => {
  console.error('Error writing to the file:', error)
})

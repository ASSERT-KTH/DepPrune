const args = process.argv.slice(2)
const project = args[0]
const client = args[1]

const repoUrl = require('get-repository-url')
const fs = require('fs')

// takes a callback
repoUrl(client, function (err, url) {
  if (err) console.log('err: ', err)
  console.log(`project: ${project}, client: ${client}`, url)
  if (url == 'null') return
  fs.appendFileSync(`${project}_dependants_url.txt`, url + '\n')
  //=> 'https://github.com/generate/generate'
  // git clone, npm i, run test, npm uninstall, run test.
  // const { spawn } = require("child_process")

  // const clientFolder = `Data/${project}_clients`

  // console.log(clientFolder)

  // // const gitCommand = spawn(`git clone ${url} ${clientFolder}  && cd ${clientFolder} && npm install && npm run test && npm uninstall ${project} && npm run test && cd ../.. `, {
  // //   shell: true
  // // })

  // const gitCommand = spawn(`git clone ${url} ${clientFolder} && cd ${clientFolder} && npm install && npm run test && cd ../.. `, {
  //   shell: true
  // })

  // console.log(`start testing the ${client} with and without ${project}`)

  // gitCommand.stdout.on("data", data => {
  //   console.log(`stdout: ${data}`)
  // })

  // gitCommand.on('error', (error) => {
  //   console.log(`error: ${error.message}`)
  // })

  // gitCommand.on("close", code => {
  //   console.log(`child process exited with code ${code}`)
  // })

})

//  or returns a promise
// repoUrl('yeoman-generator')
//   .then(function (url) {
//     console.log("generator:", url);
//     //=> 'https://github.com/generate/generate'
//   });

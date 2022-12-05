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
})

//  or returns a promise
// repoUrl('yeoman-generator')
//   .then(function (url) {
//     console.log("generator:", url);
//     //=> 'https://github.com/generate/generate'
//   });

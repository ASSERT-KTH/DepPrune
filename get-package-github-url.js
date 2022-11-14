const repoUrl = require('get-repository-url');

// takes a callback
repoUrl('body-parser', function (err, url) {
  console.log("body-parser:", url);
  //=> 'https://github.com/generate/generate'
});

//  or returns a promise
repoUrl('yeoman-generator')
  .then(function (url) {
    console.log("generator:", url);
    //=> 'https://github.com/generate/generate'
  });

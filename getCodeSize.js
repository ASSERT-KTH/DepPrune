"use strict";
exports.__esModule = true;
var fs = require("fs");
var path = require("path");
var yargs_1 = require("yargs");
var getAllFiles = function (dirname, recurse, listOfFiles) {
    if (recurse === void 0) { recurse = false; }
    if (listOfFiles === void 0) { listOfFiles = []; }
    var baseListOfFiles = fs.readdirSync(dirname);
    baseListOfFiles.forEach(function (file) {
        if (fs.statSync(dirname + "/" + file).isDirectory() && recurse) {
            listOfFiles = getAllFiles(dirname + "/" + file, recurse, listOfFiles);
        }
        else {
            listOfFiles.push(path.join(__dirname, dirname, "/", file));
        }
    });
    return listOfFiles;
};
function shouldStubbify(curPath, file, depList) {
    var shouldStub = fs.lstatSync(curPath).isFile() && file.substr(file.length - 2) == "js" && file.indexOf("externs") == -1 && file.indexOf("node_modules/@babel") == -1
        && (file.indexOf("test") == -1 || file.indexOf("node_modules") > -1);
    if (depList) {
        var node_mod_index = curPath.split("/").indexOf("node_modules");
        if (node_mod_index > -1) { // if it's a node_module and we have a dep list, need to make sure it's in the dep list 
            shouldStub = shouldStub && (depList.indexOf(curPath.split("/")[node_mod_index + 1]) > -1);
        }
    }
    return shouldStub;
}
/*
        PROJECT FLAGS
*/
var recurseThroughDirs = true;
if ((!yargs_1.argv.to_measure_size)) {
    console.log('Usage: getCodeSize.js --to_measure_size [file.js | dir] <optional: --dependencies dep_list_file>');
    process.exit(1);
}
var filename = yargs_1.argv.to_measure_size;
console.log('Reading ' + filename);
var depList;
if (yargs_1.argv.dependencies) {
    depList = fs.readFileSync(yargs_1.argv.dependencies, 'utf-8').split("\n");
}
if (fs.lstatSync(filename).isDirectory()) {
    var files = getAllFiles(filename, recurseThroughDirs);
    var totalSize_1 = 0;
    files.forEach(function (file, index) {
        // only get size of JS files (since that's all that we're stubbifying)
        var curPath = filename + file;
        curPath = file;
        if (shouldStubbify(curPath, file, depList)) { // this is all the files the stubbifyier looks at (i.e. js files, 
            totalSize_1 += fs.statSync(curPath).size; // in dependencies in node_modules or in the source code)
        }
    });
    console.log("Total size: " + totalSize_1 + " bytes");
}
else if (fs.lstatSync(filename).isFile()) {
    var totalSize = fs.statSync(filename).size;
    console.log("Total size (of one file): " + totalSize + " bytes");
}
else {
    console.log("Error: input to code size must be a directory or a file: it should be the same input as to the transformer");
}
console.log('Done');

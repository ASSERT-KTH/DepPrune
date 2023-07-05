"use strict";
exports.__esModule = true;
var fs = require("fs");
var path = require("path");
var functionLevelStubs_js_1 = require("./functionLevelStubs.js");
var functionFlagging_js_1 = require("./functionFlagging.js");
var fileLevelStubs_js_1 = require("./fileLevelStubs.js");
var ACGParseUtils_js_1 = require("./ACGParseUtils.js");
var yargs_1 = require("yargs");
var child_process_1 = require("child_process");
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
    // var shouldStub = fs.lstatSync(curPath).isFile() && file.substr(file.length - 2) == "js" && file.indexOf("externs") == -1 && file.indexOf("node_modules/@babel") == -1
    //     && (file.indexOf("test") == -1 || file.indexOf("node_modules") > -1);
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
var safeEvalMode = true; // do we try to intercept evals? default is true
if (yargs_1.argv.guarded_exec_mode == "false")
    safeEvalMode = false;
var bundlerMode = "no"; // default: don't bundle
// valid options are:
// "no" : dont bundle
// "only_bundle" : bundle but don't stub anything
// "stub_bundle" : stub an existing bundle file (this requires the bundle to have been previously created)
// "bundle_and_stub" : both stub and bundle
if (yargs_1.argv.bundler_mode)
    bundlerMode = yargs_1.argv.bundler_mode;
if (bundlerMode != "no" && bundlerMode != "only_bundle" && bundlerMode != "stub_bundle" && bundlerMode != "bundle_and_stub") {
    console.log("Invalid bundle option provided: " + bundlerMode + "; proceeding without bundling");
    bundlerMode = "no";
}
var testingMode = true; // do we add console.logs?
var recurseThroughDirs = true;
// 2 TODO
if ((!yargs_1.argv.transform) || (yargs_1.argv.callgraph && yargs_1.argv.uncovered)) {
    console.log('Usage: stubbifyRunner.js --transform [file.js | dir] [[--callgraph callgraphFile.csv] | [--uncovered coverageReport.json]] [--guarded_exec_mode [true | false]] [--bundler_mode [true | false]] [--removeFuns file_of_list_of_functions_to_completely_remove]');
    process.exit(1);
}
// 3
var filename = yargs_1.argv.transform;
console.log('Reading ' + filename);
// 4
// callgraph -- passing none fun stubs everything
var callgraphpath = yargs_1.argv.callgraph;
var coverageReportPath = yargs_1.argv.uncovered;
var removeFunsPath = yargs_1.argv.removeFuns;
var functions = [];
var listedFiles = [];
var removeFuns = [];
var noCG = true;
var uncoveredMode = !(yargs_1.argv.uncovered == undefined);
var depList;
if (callgraphpath) {
    var targets = (0, ACGParseUtils_js_1.getTargetsFromACG)(callgraphpath);
    functions = targets.map(ACGParseUtils_js_1.buildHappyName);
    listedFiles = targets.map(ACGParseUtils_js_1.getFileName);
    noCG = false;
}
var zipFiles = false; // Currently don't ever do this.
if (removeFunsPath) {
    var targetsForRemoval = (0, ACGParseUtils_js_1.getTargetsFromACG)(removeFunsPath);
    listedFiles = listedFiles.concat(targetsForRemoval.map(ACGParseUtils_js_1.getFileName));
    removeFuns = targetsForRemoval.map(ACGParseUtils_js_1.buildHappyName);
    noCG = false;
}
if (uncoveredMode) {
    var targets = (0, ACGParseUtils_js_1.getTargetsFromCoverageReport)(coverageReportPath);
    functions = targets.map(ACGParseUtils_js_1.buildHappyName);
    var all_listedFiles = targets.map(ACGParseUtils_js_1.getFileName);
    all_listedFiles.forEach(function (element) {
        if (listedFiles.indexOf(element) == -1)
            listedFiles.push(element);
    });
    noCG = false;
}
if (yargs_1.argv.dependencies) {
    depList = fs.readFileSync(yargs_1.argv.dependencies, 'utf-8').split("\n");
}
if (bundlerMode != "no") {
    if (bundlerMode == "bundle_and_stub" || bundlerMode == "only_bundle") {
        var files = getAllFiles(filename, recurseThroughDirs);
        files.forEach(function (file, index) {
            var curPath = filename + file;
            curPath = file;
            if (shouldStubbify(curPath, file, depList)) { // don't even try to stub externs
                if (noCG || listedFiles.indexOf(curPath) > -1) { // file is reachable, so only stubify functions
                    console.log("FUNCTION CASE: flagging to be stubbed: " + curPath);
                    try {
                        (0, functionFlagging_js_1.flagFunctionForStubbing)(curPath, process.cwd(), functions, uncoveredMode);
                    }
                    catch (e) {
                        console.log("ERROR: cannot stubbify function in: " + curPath);
                    }
                }
                else {
                    console.log("FILE CASE: flagging all functions to be stubbed in: " + curPath);
                    try {
                        (0, functionFlagging_js_1.flagFunctionForStubbing)(curPath, process.cwd(), [], uncoveredMode);
                    }
                    catch (e) {
                        console.log("ERROR: cannot stubbify all functions in file: " + curPath);
                        // console.log(e);
                    }
                }
            }
        });
        // By now, the functions that should be stubbed are flagged as such with 
        // eva("STUB_FLAG_STUB_THIS_STUB_FCT") as the first thing in the function body.
        // Now, we need to call the bundler.
        // To do this, we should just dispatch a shell command which invokes the bundler.
        // Notes:
        // 1. Bundler needs to be installed globally.
        // 2. Bundler needs to be called from the project being stubbified.
        // 3. Bundler config file is needed. 
        // create bundler config file
        (0, ACGParseUtils_js_1.generateBundlerConfig)(path.resolve(filename));
        // cd into project directory (filename is the path to the tgt project)
        // save current directory first to chdir back
        var stubsDir = process.cwd();
        process.chdir(path.resolve(filename));
        // install bundler dependencies
        (0, child_process_1.execSync)('npm install @rollup/plugin-node-resolve @rollup/plugin-babel @rollup/plugin-commonjs @rollup/plugin-json');
        // call bundler
        (0, child_process_1.execSync)('rollup --config rollup.stubbifier.config.js');
        // cd back into stubbifier
        process.chdir(stubsDir);
    }
    // Once bundled, we need to read in the bundle and stubbify the functions with
    // the eval.
    if (bundlerMode == "bundle_and_stub" || bundlerMode == "stub_bundle")
        (0, functionLevelStubs_js_1.functionStubFile)(path.resolve(filename) + '/stubbifyBundle.js', process.cwd(), new Map(), functions, removeFuns, uncoveredMode, safeEvalMode, testingMode, zipFiles, true);
}
else {
    // stubbing section; no bundling 
    if (fs.lstatSync(filename).isDirectory()) {
        var files = getAllFiles(filename, recurseThroughDirs);
        var unusedFiles = []
        var unusedFunctionsInFile = []
        files.forEach(function (file, index) {
            // console.log(file);
            // only stubify JS files
            // let curPath: string = filename + file;
            var curPath = file;
            // console.log("decision: " + shouldStubbify(curPath, file, depList));
            // let curAbsPath: string = process.cwd() + curPath;
            if (shouldStubbify(curPath, file, depList)) { // don't even try to stub externs
                var fileStr = curPath + '\n'
                fs.appendFileSync(`${filename}/total-files.txt`, fileStr)
                if (noCG || listedFiles.indexOf(curPath) > -1) { // file is reachable, so only stubify functions
                    console.log("FUNCTION CASE: " + curPath);
                    unusedFunctionsInFile.push(curPath)
                    var usedFileStr = curPath + '\n'
                    fs.appendFileSync(`${filename}/used-files.txt`, usedFileStr)
                    // try {
                    //     (0, functionLevelStubs_js_1.functionStubFile)(curPath, process.cwd(), new Map(), functions, removeFuns, uncoveredMode, safeEvalMode, testingMode);
                    // }
                    // catch (e) {
                    //     console.log("ERROR: cannot stubbify function in: " + curPath);
                    //     // console.log(e);
                    // }
                }
                else {
                    console.log("FILE CASE: " + curPath);
                    unusedFiles.push(curPath)
                    var unusedFileStr = curPath + '\n'
                    fs.appendFileSync(`${filename}/unused-files.txt`, unusedFileStr)
                    // try {
                    //     (0, fileLevelStubs_js_1.fileStubFile)(curPath, safeEvalMode, testingMode);
                    // }
                    // catch (e) {
                    //     console.log("ERROR: cannot stubbify file: " + curPath);
                    //     // console.log(e);
                    // }
                }
            }
        });

        // console.log('unusedFunctionsInFile: ', unusedFunctionsInFile)
        // var funcVariantsList = ACGParseUtils_js_1.getCombinations(unusedFunctionsInFile)
        // var funcVariantsLength = funcVariantsList.length
        // console.log('funcVariantsLength: ', funcVariantsLength)
        // var funcRand = ~~(Math.random() * funcVariantsLength)
        // console.log('func rand: ', funcRand)
        // var funcVariants = funcVariantsList[funcRand]
        // console.log('funcVariants: \n', funcVariants)

        // funcVariants.forEach(function (func, index) {
        //     try {
        //         (0, functionLevelStubs_js_1.functionStubFile)(func, process.cwd(), new Map(), functions, removeFuns, uncoveredMode, safeEvalMode, testingMode);
        //     }
        //     catch (e) {
        //         console.log("ERROR: cannot stubbify function in: " + func);
        //         // console.log(e);
        //     }
        // })

        console.log('unusedFiles: ', unusedFiles)
        // var fileVariantsList = ACGParseUtils_js_1.getCombinations(unusedFiles)
        // var fileVariantsLength = fileVariantsList.length
        // console.log('fileVariantsLength: ', fileVariantsLength)
        // var fileRand = ~~(Math.random() * fileVariantsLength)
        // console.log("file rand: ", fileRand)
        // var fileVariants = fileVariantsList[fileRand]
        // console.log('fileVariants: \n', fileVariants)


        // fileVariants.forEach(function (file, index) {
        //     // var line = file + '\n'
        //     // fs.appendFileSync('unusedFiles.txt', line)
        //     try {
        //         (0, fileLevelStubs_js_1.fileStubFile)(file, safeEvalMode, testingMode);
        //     }
        //     catch (e) {
        //         console.log("ERROR: cannot stubbify file: " + file);
        //         // console.log(e);
        //     }
        // })
    }
    else {
        console.log("Error: input to transformer must be a directory");
    }
}
console.log('Done');


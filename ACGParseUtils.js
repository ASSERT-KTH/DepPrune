"use strict";
exports.__esModule = true;
exports.generateBundlerConfig = exports.buildEvalCheck = exports.getFileName = exports.getTargetsFromCoverageReport = exports.getTargetsFromACG = exports.buildHappyName = void 0;
var fs = require("fs");
var babel = require("@babel/types");
var parser_1 = require("@babel/parser");
var generator_1 = require("@babel/generator");
/*
    Get an appropriate name from the UID. Appropriate for both variable
    and file names.
*/
function buildHappyName(sad) {
    var happyName = "";
    /* sanitize sad */
    sad = sad.replace(/\./g, 'dot').replace(/-/g, 'dash');
    /* take: acorn/src/location.js:<12,11>--<18,1>
       make: acorn_src_location_12_11_18_1
    */
    var split = sad.split(/.js:<|.ts:</);
    if (split.length < 2) {
        return sad;
    }
    // Do first part: acorn_src_location_
    happyName += split[0].replace(/\//g, '_') + '_';
    // Do row cols: 12_11_18_1
    happyName += split[1].substring(0, split[1].length - 1).replace(/,/g, '_').replace('>dashdash<', '_');
    return happyName;
}
exports.buildHappyName = buildHappyName;
/* Adjust the LOC (from the ACG, from QL) to match Babel.
   Code documented by example, see below. */
function adjustLOC(locAsString) {
    /* Fun(/opt/src/acorn/src/location.js:<12,12>--<18,1>)
       want
       acorn/src/location.js:<12,11>--<18,1>

       note the -1 on the first column
    */
    /* get /opt/src/acorn/src/location.js:<12,12>--<18,1> */
    var adjustedLOC = locAsString.substring(4, locAsString.length - 1);
    /* trim up to package root (by removing /opt/src/)
       get acorn/src/location.js:<12,12>--<18,1> */
    // adjustedLOC = adjustedLOC.substring("/opt/src/".length, adjustedLOC.length);
    /* adjust column number
       get acorn/src/location.js:<12,11>--<18,1> */
    var firstIndex = adjustedLOC.indexOf(":<") + ":<".length;
    var secondIndex = adjustedLOC.indexOf(">--<");
    var firstRowCol = adjustedLOC.substring(firstIndex, secondIndex).split(',');
    firstRowCol[1] = String(Number(firstRowCol[1]) - 1);
    adjustedLOC = adjustedLOC.substring(0, firstIndex) + firstRowCol[0] + ',' + firstRowCol[1] +
        adjustedLOC.substring(secondIndex);
    return adjustedLOC;
}
/*
    Parse an Approximate Call Graph (ACG) .csv file, and produce a string[] with
    file and source information for calls which the ACG picked up on.

    Note: You may want to cross-reference this list with a list of callable functions, probably.
*/
function getTargetsFromACG(filepath) {
    var unprocessedCG = fs.readFileSync(filepath, 'utf-8').split('\n');
    /* remove header */
    unprocessedCG.shift();
    var targets = unprocessedCG.map(function (line) {
        line = line.substr(1, line.length - 2);
        var target = line.split('\",\"')[1];
        if (!target || target.substr(0, 3) != 'Fun') {
            return "";
        }
        return adjustLOC(target);
    });
    var partialRet = targets.filter(function (line) {
        return line != "";
    });
    /*
    let mapObj = {};

    // construct return map
    partialRet.forEach(s => {
        mapObj[s] = "";
    });

    return new Map(Object.entries(mapObj));
    */
    return partialRet;
}
exports.getTargetsFromACG = getTargetsFromACG;
function getUncoveredFunctions(pathToCoverageReport) {
    var coverage = require(pathToCoverageReport);
    var calledFunctions = [];
    var uncalledFunctions = [];
    Object.keys(coverage).forEach(function (fileName) {
        Object.keys(coverage[fileName].fnMap).forEach(function (key) {
            if (coverage[fileName].f[key] > 0) {
                var loc = coverage[fileName].fnMap[key].loc;
                calledFunctions.push(fileName + ":<" + loc.start.line + "," + loc.start.column + ">--<" + loc.end.line + "," + loc.end.column + ">");
            }
            else {
                var loc = coverage[fileName].fnMap[key].loc;
                uncalledFunctions.push(fileName + ":<" + loc.start.line + "," + loc.start.column + ">--<" + loc.end.line + "," + loc.end.column + ">");
            }
        });
    });
    // console.log('calledFunctions: ', calledFunctions);
    // console.log('uncalledFunctions: ', uncalledFunctions);
    return calledFunctions;
}
/*
[
  'Fun(/Users/Alexi/Documents/Projects/JSTransformationBenchmarks/razorpay-node/distrazorpay.js:<16,11>--<19,5>)',
  ...
]
*/
function getTargetsFromCoverageReport(filepath) {
    var uncoveredFunctions = getUncoveredFunctions(filepath);
    return uncoveredFunctions;
}
exports.getTargetsFromCoverageReport = getTargetsFromCoverageReport;
function getFileName(target) {
    return target.split(":")[0];
}
exports.getFileName = getFileName;
function buildEvalCheck(callExpNode, inAsyncFct, filename) {
    // if ( callee === eval ) { console.warn("BTW dangerous call"); }
    // "let dangerousFunctions = [eval, process.exec];"
    // ( () => let tempExp__uniqID = callee; if( tempExp__uniqID === eval) { console.warn("uh oh"); } return tempExp__uniqID; )()
    var tempVarID = babel.identifier("tempExp__uniqID");
    var tempVarDecl = babel.variableDeclaration("let", [babel.variableDeclarator(tempVarID, callExpNode.callee)]);
    var tempVarDecls = [tempVarDecl];
    if (callExpNode.callee.type == "MemberExpression" && (callExpNode.callee.property.type == "Identifier" || callExpNode.callee.property.type == "PrivateName")) {
        // If it's a memberExpression, we want to save the receiver.
        var tempReceiverID = babel.identifier("tempEXP__rec__uniqID");
        var tempReceiver = babel.variableDeclaration("let", [babel.variableDeclarator(tempReceiverID, callExpNode.callee.object)]);
        // callee.bind(callee.object)
        var tempBindCall = babel.callExpression(babel.memberExpression(babel.memberExpression(tempReceiverID, callExpNode.callee.property, callExpNode.callee.computed), babel.identifier("bind")), [tempReceiverID]);
        tempBindCall.isNewCallExp = true;
        tempVarDecl = babel.variableDeclaration("let", [babel.variableDeclarator(tempVarID, tempBindCall)]);
        tempVarDecls = [tempReceiver, tempVarDecl];
    }
    var intermCallExp = babel.callExpression(babel.memberExpression(babel.identifier("dangerousFunctions"), babel.identifier("indexOf")), [tempVarID]);
    intermCallExp.isNewCallExp = true;
    var test = babel.binaryExpression(">", intermCallExp, babel.numericLiteral(-1));
    var consequent = babel.expressionStatement(babel.callExpression(babel.memberExpression(babel.identifier("console"), babel.identifier("warn")), [babel.stringLiteral("[STUBBIFIER METRICS] WARNING: Dangerous call in expanded stub, in file: " + filename)]));
    consequent.expression.isNewCallExp = true;
    var ifCheckStmt = babel.ifStatement(test, consequent);
    var retCallExp = babel.callExpression(callExpNode.callee /*tempVarID*/, callExpNode.arguments);
    retCallExp.isNewCallExp = true;
    var returnStmt = babel.returnStatement(retCallExp);
    var arrowFunc = babel.arrowFunctionExpression([], // params
    babel.blockStatement(tempVarDecls.concat([ifCheckStmt, returnStmt])), inAsyncFct); // whether or not it should be async
    return babel.callExpression(arrowFunc, []);
}
exports.buildEvalCheck = buildEvalCheck;
// generate rollup.stubbifier.config.js in the directory specified
function generateBundlerConfig(dirname) {
    /*
        export default {
          input: 'name of the main file in package.json',
          output: {
            dir: 'output',
            format: 'cjs'
          },
          context: 'null',
          moduleContext: 'null',
          plugins: [nodeResolve({ moduleDirectories: ['node_modules'] }), commonjs(), babel()]
        };
    */
    var mainPath = undefined;
    try {
        var json = JSON.parse(fs.readFileSync(dirname + "/package.json", 'utf-8'));
        mainPath = json.main;
    }
    catch (e) { } // if there's an error, then we're not using esm
    if (!mainPath) {
        mainPath = "index.js";
    }
    var configBody = "import nodeResolve from '@rollup/plugin-node-resolve';\n     import babel from '@rollup/plugin-babel';\n     import commonjs from '@rollup/plugin-commonjs';\n     import json from '@rollup/plugin-json';\n\n     export default {\n          input: '" + mainPath + "',\n          output: {\n            file: 'stubbifyBundle.js',\n            format: 'cjs'\n          },\n          context: 'null',\n          moduleContext: 'null',\n          plugins: [nodeResolve({ moduleDirectories: ['node_modules'] }), commonjs(), babel(), json()]\n        };";
    configBody = generator_1["default"](parser_1.parse(configBody, { sourceType: "unambiguous" }).program).code;
    fs.writeFileSync(dirname + "/rollup.stubbifier.config.js", configBody);
}
exports.generateBundlerConfig = generateBundlerConfig;

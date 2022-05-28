"use strict";
exports.__esModule = true;
exports.flagFunctionForStubbing = void 0;
var fs = require("fs");
var parser_1 = require("@babel/parser");
var generator_1 = require("@babel/generator");
var core_1 = require("@babel/core");
var ACGParseUtils_js_1 = require("./ACGParseUtils.js");
var MIN_FCT_STUB_LENGTH = 5; // only stub functions that are > 5 lines long
// transform the function if: 
// the list of functions to stub is empty (this defaults to the entire set of top level functions in the file -- TODO probably only DEBUG MODE)
// or, if the function name is in the list
// TODO deal with scoping
function shouldTransformFunction(fctName, reachableFuns) {
    var fctNotInList = (reachableFuns.indexOf(fctName) == -1);
    return fctNotInList;
    // Trying to reverse the logic.
    // return uncoveredMode? ! fctNotInList : fctNotInList;
}
function getNumLinesSpannedByNode(n) {
    return n.loc.end.line - n.loc.start.line;
}
function generateNodeUID(n, filename, coverageMode) {
    // acorn/src/location.js:<12,12>--<18,1>
    var locString;
    if (!coverageMode)
        locString = "<" + n.loc.start.line + "," + n.loc.start.column + ">--<" + n.loc.end.line + "," + n.loc.end.column + ">";
    else {
        locString = "<" + n.body.loc.start.line + "," + n.body.loc.start.column + ">--<" + n.body.loc.end.line + "," + n.body.loc.end.column + ">";
    }
    return ACGParseUtils_js_1.buildHappyName(filename + ":" + locString);
}
// generated with babeljs_gen_gen
function get_stub_flag() {
    var node_map = {};
    node_map["new_StringLiteral_4"] = {
        type: "StringLiteral",
        value: "STUB_FLAG_STUB_THIS_STUB_FCT"
    };
    node_map["new_Identifier_3"] = {
        type: "Identifier",
        name: "eval"
    };
    node_map["new_CallExpression_2"] = {
        type: "CallExpression",
        callee: node_map["new_Identifier_3"],
        arguments: Array(node_map["new_StringLiteral_4"])
    };
    node_map["new_ExpressionStatement_1"] = {
        type: "ExpressionStatement",
        expression: node_map["new_CallExpression_2"]
    };
    return node_map["new_ExpressionStatement_1"];
}
/*
    processAST: do it
*/
function processASTForFlagging(ast, reachableFuns, filename, uncoveredMode) {
    // let funcMap : Map<string, [babel.Identifier[], babel.BlockStatement]> = new Map();
    var supportedFunctionNodes = [
        "FunctionExpression",
        "FunctionDeclaration",
        "ArrowFunctionExpression",
        "ClassMethod",
        "ObjectMethod",
    ];
    var output = core_1.transformFromAstSync(ast, null, { ast: true, plugins: [function processASTForFlagging() {
                return { visitor: {
                        Function: function (path) {
                            // let inFunction: boolean = path.findParent((path) => path.isFunction());
                            if (supportedFunctionNodes.indexOf(path.node.type) > -1 /*&& ! inFunction*/ && getNumLinesSpannedByNode(path.node) > MIN_FCT_STUB_LENGTH) {
                                // let functionUIDName = "global::" + path.node.id.name;
                                var functionUIDName = generateNodeUID(path.node, filename, uncoveredMode);
                                // don't forget to write out function body before we replace
                                if (shouldTransformFunction(functionUIDName, reachableFuns)) {
                                    // console.log("Triggered stubbification.");
                                    if (path.node.kind == "constructor" || path.node.generator || path.node.async) { // TODO broken for generators 
                                        path.skip(); // don't transform a constructor or anything in a constructor (stubs dont work with "super" and "this")
                                    }
                                    else {
                                        var flaggedParent = path.findParent(function (path) { return path.node.isFlagged; });
                                        if (!flaggedParent) {
                                            var flaggingStmt = get_stub_flag();
                                            path.node.body.body = [flaggingStmt].concat(path.node.body.body);
                                            path.node.isFlagged = true;
                                        }
                                    }
                                }
                            }
                        }
                    } };
            }] });
    return output.ast;
}
function flagFunctionForStubbing(filename, stubspath, reachableFuns, uncoveredMode) {
    // save the old file 
    // this might get removed later, but is useful right now for debugging
    fs.copyFileSync(filename, filename + ".original");
    var code = fs.readFileSync(filename, 'utf-8');
    // let origCodeFileName: string = process.cwd() + "/" + filename + ".BIGG";
    var ast;
    var esmMode = false;
    try {
        ast = parser_1.parse(code, { sourceType: "unambiguous", plugins: ["classProperties", "typescript"] }).program;
        esmMode = ast.sourceType == "module";
    }
    catch (e) {
        console.error("Yikes... parsing error in " + filename + ":  " + e);
        return;
    }
    // Preprocess the AST, propagating function ID information to FunctionExpressions.
    ast = processASTForFlagging(ast, reachableFuns, filename, uncoveredMode);
    // console.log(generate(ast).code)
    // write out the stub, overwriting the old file
    fs.writeFileSync(filename, generator_1["default"](ast).code);
}
exports.flagFunctionForStubbing = flagFunctionForStubbing;

"use strict";
exports.__esModule = true;
exports.functionStubFile = void 0;
var fs = require("fs");
var parser_1 = require("@babel/parser");
var generator_1 = require("@babel/generator");
var core_1 = require("@babel/core");
var babel = require("@babel/types");
var tar = require("tar");
var path = require("path");
var ACGParseUtils_js_1 = require("./ACGParseUtils.js");
var MIN_FCT_STUB_LENGTH = 5; // only stub functions that are > 5 lines long
// transform the function if: 
// the list of functions to stub is empty (this defaults to the entire set of top level functions in the file -- TODO probably only DEBUG MODE)
// or, if the function name is in the list
// TODO deal with scoping
function shouldTransformFunction(fctName, reachableFuns, uncoveredMode, fctNode) {
    var fctNotInList = (reachableFuns.indexOf(fctName) == -1);
    if (fctNode.body.type == "BlockStatement") {
        fctNotInList = fctNotInList && (!(0, generator_1["default"])(fctNode.body.body[0]).code.startsWith('eval("STUBBIFIER_DONT_STUB_ME");'));
    }
    return fctNotInList;
}
// Remove a function if it is specified in the list of functions to remove.
function shouldRemoveFunction(fctName, removeFuns) {
    return removeFuns.indexOf(fctName) != -1;
}
function shouldTransformBundlerMode(fctNode) {
    if (fctNode.body.type == "BlockStatement") {
        return (0, generator_1["default"])(fctNode.body.body[0]).code == 'eval("STUB_FLAG_STUB_THIS_STUB_FCT");';
    }
    return false;
}
function generateNodeUID(n, filename, coverageMode) {
    // acorn/src/location.js:<12,12>--<18,1>
    var locString;
    if (!coverageMode)
        locString = "<" + n.loc.start.line + "," + n.loc.start.column + ">--<" + n.loc.end.line + "," + n.loc.end.column + ">";
    else {
        locString = "<" + n.body.loc.start.line + "," + n.body.loc.start.column + ">--<" + n.body.loc.end.line + "," + n.body.loc.end.column + ">";
    }
    return (0, ACGParseUtils_js_1.buildHappyName)(filename + ":" + locString);
}
function getNumLinesSpannedByNode(n) {
    return n.loc.end.line - n.loc.start.line;
}
/*
    processAST: do it
*/
function processAST(ast, functionsToStub, reachableFuns, filename, uncoveredMode, safeEvalMode, bundlerMode, removeFuns) {
    if (safeEvalMode === void 0) { safeEvalMode = false; }
    if (bundlerMode === void 0) { bundlerMode = false; }
    // let funcMap : Map<string, [babel.Identifier[], babel.BlockStatement]> = new Map();
    var supportedFunctionNodes = [
        "FunctionExpression",
        "FunctionDeclaration",
        "ArrowFunctionExpression",
        "ClassMethod",
        "ObjectMethod",
    ];
    var output = (0, core_1.transformFromAstSync)(ast, null, { ast: true, plugins: [function processAST() {
                return { visitor: {
                        Function: function (path) {
                            // let inFunction: boolean = path.findParent((path) => path.isFunction());
                            if (supportedFunctionNodes.indexOf(path.node.type) > -1 /*&& ! inFunction*/ && getNumLinesSpannedByNode(path.node) > MIN_FCT_STUB_LENGTH) {
                                // let functionUIDName = "global::" + path.node.id.name;
                                var functionUIDName = generateNodeUID(path.node, filename, uncoveredMode);
                                // don't forget to write out function body before we replace
                                if (shouldRemoveFunction(functionUIDName, removeFuns)) {
                                    // This if is duplicated from below.
                                    if (path.node.kind == "constructor" || path.node.generator || path.node.async) { // TODO broken for generators -- is this true?
                                        path.skip(); // don't transform a constructor or anything in a constructor (stubs dont work with "super" and "this")
                                    }
                                    else {
                                        path.node.body = babel.blockStatement([babel.throwStatement(babel.newExpression(babel.identifier("Error"), [babel.stringLiteral('[Stubbifier] Function was removed!')]))]);
                                    }
                                }
                                else if ((bundlerMode && shouldTransformBundlerMode(path.node)) || (shouldTransformFunction(functionUIDName, reachableFuns, uncoveredMode, path.node))) {
                                    if (path.node.kind == "constructor" || path.node.generator || path.node.async) { // TODO broken for generators -- is this true?
                                        path.skip(); // don't transform a constructor or anything in a constructor (stubs dont work with "super" and "this")
                                    }
                                    else {
                                        var inClassOrObjMethod = path.findParent(function (path) {
                                            if (path.isClassMethod() || path.isObjectMethod())
                                                return path;
                                        });
                                        if (path.node.type == "ClassMethod" || path.node.type == "ObjectMethod" || inClassOrObjMethod) {
                                            // It's a constructor, getter, or setter.
                                            var afun = babel.arrowFunctionExpression(path.node.params, path.node.body, path.node.async);
                                            functionsToStub.set(functionUIDName, (0, generator_1["default"])(afun).code);
                                            if (path.node.type == "ClassMethod" || path.node.type == "ObjectMethod") {
                                                if (!path.node.key.name) {
                                                    path.node.body = generateNewClassMethodNoID(functionUIDName, path.node.key, path.node.type == "ArrowFunctionExpression");
                                                }
                                                else {
                                                    path.node.body = generateNewClassMethodWithID(functionUIDName, path.node.key.name, path.node.kind, path.node.type == "ArrowFunctionExpression");
                                                }
                                            }
                                            else { // this is the inClassOrObjMethod
                                                if (path.node.id && path.node.id.name) {
                                                    path.node.body = generateNewFunctionWithID(functionUIDName, path.node.id.name, path.node.type == "ArrowFunctionExpression");
                                                }
                                                else {
                                                    // can't do the transformation if there's no name. because, there is no way to 
                                                    // refer to a function with no name, inside a class method. our normal strategy of using "this" doesn't
                                                    // work since inside a class it would refer to the class instance
                                                    functionsToStub["delete"](functionUIDName); // delete from map -- needed to add first bc path.node.body changes
                                                    path.skip();
                                                }
                                            }
                                        }
                                        else {
                                            functionsToStub.set(functionUIDName, (0, generator_1["default"])(path.node).code);
                                            var forbiddenFunctionReassignments = [
                                                "VariableDeclarator",
                                                "CallExpression",
                                                "AssignmentExpression",
                                                "ReturnStatement",
                                                "ObjectProperty"
                                            ];
                                            path.node.body = (path.node.id && path.node.id.name && (forbiddenFunctionReassignments.indexOf(path.parentPath.node.type) == -1)) ?
                                                generateNewFunctionWithID(functionUIDName, path.node.id.name, path.node.type == "ArrowFunctionExpression") :
                                                generateNewFunctionNoID(functionUIDName, path.node.type == "ArrowFunctionExpression");
                                            if (path.node.type == "ArrowFunctionExpression") {
                                                path.node.params = [babel.restElement(babel.identifier("args_uniqID"))];
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } };
            }] });
    return output.ast;
}
// if we know the function ID, then we can reassign it from inside itself
function generateNewFunctionWithID(scopedFctName, fctID, isArrowFunction) {
    if (isArrowFunction === void 0) { isArrowFunction = false; }
    var argsName = isArrowFunction ? "args_uniqID" : "arguments";
    var newFunctionBodyString = "let toExec = eval(stubs.getCode(\"".concat(scopedFctName, "\"));\n\t\t\t\t\t\t\t\t\t\t toExec = stubs.copyFunctionProperties(").concat(fctID, ", toExec);\n\t\t\t\t\t\t\t\t\t     ").concat(fctID, " = toExec;\n\t\t\t\t\t\t\t\t\t     return toExec.apply(this, ").concat(argsName, ");");
    return babel.blockStatement((0, parser_1.parse)(newFunctionBodyString, { allowReturnOutsideFunction: true, sourceType: "unambiguous",
        plugins: ["classProperties"] }).program.body);
}
// if the function does not have an ID (i.e. an anonymous function) or if the ID is not an identifier (i.e. a dynamically named function)
// then, we need to store it in the stubsmap
function generateNewFunctionNoID(scopedFctName, isArrowFunction) {
    if (isArrowFunction === void 0) { isArrowFunction = false; }
    var argsName = isArrowFunction ? "args_uniqID" : "arguments";
    var newFunctionBodyString = "let fctID = \"".concat(scopedFctName, "\";\n\t\t\t\t\t\t\t\t\t     let toExecString = stubs.getStub(fctID);\n\t\t\t\t\t\t\t\t\t     if (! toExecString) {\n\t\t\t\t\t\t\t\t\t       toExecString = stubs.getCode(fctID);\n\t\t\t\t\t\t\t\t\t       stubs.setStub(fctID, toExecString);\n\t\t\t\t\t\t\t\t\t     }\n\t\t\t\t\t\t\t\t\t     let toExec = eval(toExecString);\n\t\t\t\t\t\t\t\t\t     toExec = stubs.copyFunctionProperties(this, toExec);\n        \t\t\t\t\t\t\t\t toExec.stubbifierExpandedStub = true;\n\t\t\t\t\t\t\t\t\t     return toExec.apply(this, ").concat(argsName, ");");
    return babel.blockStatement((0, parser_1.parse)(newFunctionBodyString, { allowReturnOutsideFunction: true, sourceType: "unambiguous",
        plugins: ["classProperties"] }).program.body);
}
// for class methods, we can redefine them from inside themselves
// but the format is different from nonclass methods: we need to use this.__proto__.ID
function generateNewClassMethodWithID(scopedFctName, fctID, kind, isArrowFunction) {
    if (isArrowFunction === void 0) { isArrowFunction = false; }
    var argsName = isArrowFunction ? "args_uniqID" : "arguments";
    var fctDefString = "this.".concat(fctID, " = toExec;"); // default callExpression
    var fctLookupString = "this.".concat(fctID);
    switch (kind) {
        case "get":
            fctDefString = "this.__defineGetter__(\"".concat(fctID, "\", toExec);");
            fctLookupString = "this.__lookupGetter__(\"".concat(fctID, "\")");
            break;
        case "set":
            fctDefString = "this.__defineSetter__(\"".concat(fctID, "\", toExec);");
            fctLookupString = "this.__lookupSetter__(\"".concat(fctID, "\")");
            break;
    }
    var newFunctionBodyString = "let toExec = eval(stubs.getCode(\"".concat(scopedFctName, "\"));\n\t\t\t\t\t\t\t\t\t\t toExec = stubs.copyFunctionProperties(").concat(fctLookupString, ", toExec);\n\t\t\t\t\t\t\t\t\t     ").concat(fctDefString, "\n\t\t\t\t\t\t\t\t\t     return toExec.apply(this, ").concat(argsName, ");");
    return babel.blockStatement((0, parser_1.parse)(newFunctionBodyString, { allowReturnOutsideFunction: true, sourceType: "unambiguous",
        plugins: ["classProperties"] }).program.body);
}
function generateNewClassMethodNoID(scopedFctName, key, isArrowFunction) {
    if (isArrowFunction === void 0) { isArrowFunction = false; }
    var argsName = isArrowFunction ? "args_uniqID" : "arguments";
    var newFunctionBodyString = "let fctID = \"".concat(scopedFctName, "\";\n\t\t\t\t\t\t\t\t\t\t let toExecString = stubs.getStub(fctID);\n\t\t\t\t\t\t\t\t\t\t if (! toExecString) {\n\t\t\t\t\t\t\t\t\t       toExec = stubs.getCode(fctID);\n\t\t\t\t\t\t\t\t\t       stubs.setStub(fctID, toExecString);\n\t\t\t\t\t\t\t\t\t     }\n\t\t\t\t\t\t\t\t\t     let toExec = eval(toExecString);\n\t\t\t\t\t\t\t\t\t     toExec = stubs.copyFunctionProperties(this[").concat((0, generator_1["default"])(key).code, "], toExec);\n\t\t\t\t\t\t\t\t\t     return toExec.apply(this, ").concat(argsName, ");");
    return babel.blockStatement((0, parser_1.parse)(newFunctionBodyString, { allowReturnOutsideFunction: true, sourceType: "unambiguous",
        plugins: ["classProperties"] }).program.body);
}
function stubifyFile(filename, stubspath, functionsToStub, reachableFuns, removeFuns, uncoveredMode, safeEvalMode, testingMode, zipFiles, bundleMode) {
    if (safeEvalMode === void 0) { safeEvalMode = false; }
    if (testingMode === void 0) { testingMode = false; }
    if (zipFiles === void 0) { zipFiles = false; }
    if (bundleMode === void 0) { bundleMode = false; }
    // save the old file 
    // this might get removed later, but is useful right now for debugging
    fs.copyFileSync(filename, filename + ".original");
    var code = fs.readFileSync(filename, 'utf-8');
    // let origCodeFileName: string = process.cwd() + "/" + filename + ".BIGG";
    var ast;
    var esmMode = false;
    try {
        ast = (0, parser_1.parse)(code, { sourceType: "unambiguous", plugins: ["classProperties", "typescript"] }).program;
        esmMode = ast.sourceType == "module";
    }
    catch (e) {
        console.error("Yikes... parsing error in " + filename + ":  " + e);
        return;
    }
    // Preprocess the AST, propagating function ID information to FunctionExpressions.
    ast = processAST(ast, functionsToStub, reachableFuns, filename, uncoveredMode, safeEvalMode, bundleMode, removeFuns);
    var setup_stubs = "let stubs = new (require('" + stubspath + "/stubbifier_cjs.cjs'))('" + filename + "', " + testingMode + ");";
    if (esmMode) {
        setup_stubs = "import {default as stubs_fct} from '" + stubspath + "/stubbifier_es6.mjs'; let stubs = new stubs_fct('" + filename + "', " + testingMode + ");";
    }
    ast = (0, core_1.transformFromAstSync)(ast, null, { ast: true,
        plugins: [
            function visitAndAddStubsSetup() {
                return {
                    visitor: {
                        Program: function (path) {
                            path.node.body = ((0, parser_1.parse)(setup_stubs, { sourceType: "unambiguous" }).program.body).concat(path.node.body);
                            path.skip();
                        }
                    }
                };
            }
        ]
    }).ast;
    // console.log(generate(ast).code)
    // write out the stub, overwriting the old file
    fs.writeFileSync(filename, (0, generator_1["default"])(ast).code.split('eval("STUB_FLAG_STUB_THIS_STUB_FCT");').join("\n"));
    // make the directory, so there can be a file added to it for each function processed
    // only create the dir if it doesn't already exist
    if (!fs.existsSync(filename + ".dir")) {
        fs.mkdirSync(filename + ".dir");
    }
    // then, write out all the functions to be stubbified 
    // forEach for a map iterates over: value, key
    functionsToStub.forEach(function (fctBody, fctName, map) {
        if (bundleMode) {
            fctBody = fctBody.split('eval("STUB_FLAG_STUB_THIS_STUB_FCT");').join("\n");
        }
        var stubFileBody = "let " + fctName + " = " + fctBody + "; \n\n" + fctName + ";";
        // TODO: currently in safeEvalMode we check to see if console.log is eval
        if (testingMode) {
            console.log("[STUBBIFIER METRICS] function stubbed: ".concat(fctName, " --- ").concat(filename));
            stubFileBody = "console.log(\"[STUBBIFIER METRICS] EXPANDED STUB HAS BEEN CALLED: ".concat(fctName, " --- ").concat(filename, "\");") + stubFileBody;
        }
        if (safeEvalMode) {
            stubFileBody = "let dangerousFunctions = [eval]; if( process){dangerousFunctions += [process.exec]};\n" + stubFileBody;
        }
        /* debug */
        // let fileSpecAST = parse(stubFileBody, {sourceType: "unambiguous", plugins: [ "classProperties"]}).program;
        var fileSpecAST = {};
        try {
            fileSpecAST = (0, parser_1.parse)(stubFileBody, { allowSuperOutsideMethod: true, sourceType: "unambiguous", plugins: ["classProperties"] }).program;
        }
        catch (e) {
            console.error("Big oof bro... error parsing following snippet. Error: " + e);
            console.error(stubFileBody);
            process.exit(0);
        }
        fileSpecAST = (0, core_1.transformFromAstSync)(fileSpecAST, null, { ast: true, plugins: [function addTests() {
                    return { visitor: {
                            CallExpression: function (path) {
                                if (safeEvalMode && !path.node.isNewCallExp && !(path.node.callee.type == "Super")) {
                                    //let enclosingStmtNode = path.findParent((path) => path.isStatement());
                                    //enclosingStmtNode.insertBefore(buildEvalCheck(path.node));
                                    var inAsyncFunction = path.findParent(function (path) { return path.isFunction() && path.node.async; });
                                    var newWrapperCall = (0, ACGParseUtils_js_1.buildEvalCheck)(path.node, inAsyncFunction, filename);
                                    newWrapperCall.isNewCallExp = true;
                                    path.replaceWith(newWrapperCall);
                                }
                            }
                        } };
                }] }).ast;
        fs.writeFileSync(filename + ".dir/" + fctName + ".BIGG", (0, generator_1["default"])(fileSpecAST).code);
        // console.log(fctBody);
    });
    // Now that the directory is written, zip it up (if we want to).
    if (zipFiles) {
        var justFile = path.basename(filename);
        var pathToFile = path.dirname(filename);
        tar.c({
            gzip: true,
            sync: true,
            cwd: process.cwd() + '/' + pathToFile
        }, [justFile + ".dir"]).pipe(fs.createWriteStream(filename + ".dir" + '.tgz'));
        // Once zipped, delete the existing directory.
        fs.rmdirSync(filename + ".dir", { recursive: true });
    }
}
exports.functionStubFile = stubifyFile;

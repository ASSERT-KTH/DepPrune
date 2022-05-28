"use strict";
exports.__esModule = true;
exports.fileStubFile = void 0;
var fs = require("fs");
var parser_1 = require("@babel/parser");
var generator_1 = require("@babel/generator");
var core_1 = require("@babel/core");
var babel = require("@babel/types");
var zlib = require("zlib");
var stream_1 = require("stream");
var ACGParseUtils_js_1 = require("./ACGParseUtils.js");
var MIN_FILE_STUB_LENGTH = 5; // only stub files that are > 5 lines
// moving import statements to the original code
function processAST(ast, importStmts, exportStmts, filename, safeEvalMode) {
    if (safeEvalMode === void 0) { safeEvalMode = false; }
    // console.log(code);
    var output = core_1.transformFromAstSync(ast, null, { ast: true, plugins: [function processPlugin() {
                return { visitor: {
                        CallExpression: function (path) {
                            if (safeEvalMode && !path.node.isNewCallExp && !(path.node.callee.type == "Super")) {
                                //let enclosingStmtNode = path.findParent((path) => path.isStatement());
                                //enclosingStmtNode.insertBefore(buildEvalCheck(path.node));
                                var inAsyncFunction = path.findParent(function (path) { return path.isFunction() && path.node.async; });
                                var newWrapperCall = ACGParseUtils_js_1.buildEvalCheck(path.node, inAsyncFunction, filename);
                                newWrapperCall.isNewCallExp = true;
                                path.replaceWith(newWrapperCall);
                            }
                        },
                        /*
                            Deal with imports.
                            Imports *always* stay in the original file, and they never modify anything.
                        */
                        ImportDeclaration: function (path) {
                            importStmts.push(path.node); // put node into stmt move list
                            path.remove(); // yeet the node into the void
                            path.skip();
                        },
                        /*
                            Deal with exports.
                            There are multiple different kinds of exports, and in some cases we need to leave
                            part of the export to ensure that e.g. certain variables remain in scope.
                
                            e.g.
                            export const exportFoo = foo;
                
                            Here, we need to leave `const exportFoo = foo`, as the assignment makes `exportFoo`
                            available in the subsequent scope.
                        */
                        ExportDefaultDeclaration: function (path) {
                            // Check if export has a declaration.
                            if (path.node.declaration !== null) {
                                // Construct new node based on the export.
                                // Save the declaration that we're going to replace.
                                var savedDeclaration = path.node.declaration; // the actual type here is a giant union type (88 members, don't feel like typing it)
                                exportStmts["default"].push(path.node);
                                // Remove the declaration.
                                // path.node.declaration = null;
                                // previous line of code not required: we always replace the declaration with something else
                                // and, babel will not allow the ExportDefaultDeclaration to have a null declaration
                                // Modify path.node to have the appropriate exports, based on the type of export it is.
                                switch (savedDeclaration.type) {
                                    case "ClassDeclaration":
                                        // TODO: Doing the same thing twice for local and exported. Ensure that this is what we want.
                                        path.node.declaration = savedDeclaration.id;
                                        path.replaceWith(savedDeclaration);
                                        break;
                                    case "FunctionDeclaration":
                                        path.node.declaration = savedDeclaration.id;
                                        path.replaceWith(savedDeclaration);
                                        break;
                                    default:
                                        path.remove(); // in babel, identifiers count as declarations
                                    // 	path.node.declaration = savedDeclaration; // I don't think you can have a vardecl as a default export ...?
                                    /* TODO: more cases */
                                }
                            }
                            else {
                                // this might be unreachable with babel, but keep it around just in case
                                exportStmts["default"].push(path.node);
                                path.remove();
                            }
                            // return false;
                            path.skip();
                        },
                        ExportNamedDeclaration: function (path) {
                            // Check if export has a declaration.
                            if (path.node.declaration !== null) {
                                // Construct new node based on the export.
                                // Save the declaration that we're going to replace.
                                var savedDeclaration = path.node.declaration;
                                // Remove the declaration.
                                // path.node.declaration.parentPath.remove();
                                path.node.declaration = null;
                                // Modify path.node to have the appropriate exports, based on the type of export it is.
                                switch (savedDeclaration.type) {
                                    case "ClassDeclaration":
                                        // TODO: Doing the same thing twice for local and exported. Ensure that this is what we want.
                                        // need to have 2 different identifiers, to avoid shallow copy issues
                                        path.node.specifiers.push(babel.exportSpecifier(babel.identifier(savedDeclaration.id.name), babel.identifier(savedDeclaration.id.name)));
                                        break;
                                    case "FunctionDeclaration":
                                        path.node.specifiers.push(babel.exportSpecifier(babel.identifier(savedDeclaration.id.name), babel.identifier(savedDeclaration.id.name)));
                                        break;
                                    case "VariableDeclaration":
                                        var lsd = savedDeclaration;
                                        for (var _i = 0, _a = lsd.declarations; _i < _a.length; _i++) {
                                            var v = _a[_i];
                                            /* There are only two cases here: VariableDeclator (which is horrible), and Identifier (cleaner). */
                                            /* TODO: currently just casting the .id to an Identifier, even though it's
                                                a PatternKind.
                                            
                                                Change to deal with other possible PatternKinds.
                                            */
                                            switch (v.id.type) {
                                                case "Identifier":
                                                    var idAsIdentifierLocal = babel.identifier(v.id.name);
                                                    var idAsIdentifierExport = babel.identifier(v.id.name);
                                                    path.node.specifiers.push(babel.exportSpecifier(idAsIdentifierLocal, idAsIdentifierExport));
                                                    break;
                                                case "ObjectPattern":
                                                    var idAsObjectPattern = v.id;
                                                    idAsObjectPattern.properties.map(function (v) {
                                                        /* v has to have type Identifier as per destructured assignment specification */
                                                        var propertyAsExportIdentifier = v.key;
                                                        path.node.specifiers.push(babel.exportSpecifier(propertyAsExportIdentifier, propertyAsExportIdentifier));
                                                    });
                                                    break;
                                                default:
                                                    console.error("Unexpected case of VariableDeclarator: " + v.id.type);
                                                    process.exit(1);
                                            }
                                        }
                                        break;
                                    /* TODO: more cases */
                                }
                                exportStmts["named"].push(path.node);
                                // Replace it with the declaration.
                                path.replaceWith(savedDeclaration);
                            }
                            else {
                                exportStmts["named"].push(path.node);
                                path.remove();
                            }
                            path.skip();
                        }
                    } };
            }] });
    return output.ast;
}
// TODO: stubbify, not stubify
function stubifyFile(filename, safeEvalMode, testingMode, zipFiles) {
    if (safeEvalMode === void 0) { safeEvalMode = false; }
    if (testingMode === void 0) { testingMode = false; }
    if (zipFiles === void 0) { zipFiles = false; }
    // save the old file 
    // this might get removed later, but is useful right now for debugging
    fs.copyFileSync(filename, filename + ".original");
    var code = fs.readFileSync(filename, 'utf-8');
    // check if the file is long enough to bother stubbifying
    if ((code.match(/\n/g) || []).length < MIN_FILE_STUB_LENGTH) {
        return;
    }
    var origCodeFileName = filename + ".BIGG";
    var ast;
    var esmMode;
    try {
        ast = parser_1.parse(code, { sourceType: "unambiguous", plugins: ["classProperties", "typescript"] }).program;
        esmMode = ast.sourceType == "module";
    }
    catch (e) {
        console.error("Yikes... parsing error in " + filename + ":  " + e);
        return;
    }
    var importStmts = [];
    var exportStmts = { "default": [], "named": [] };
    ast = processAST(ast, importStmts, exportStmts, filename, safeEvalMode);
    var requires = "const fs_uniqID = require('fs'); const zlib_uniqID = require('zlib');";
    if (esmMode) {
        requires = "import * as fs_uniqID from 'fs'; import * as zlib_uniqID from 'zlib';";
    }
    // TODO: kinda dumb that we unzip then reread but ok for now.
    var body = "\n\t\tif (!fs_uniqID.existsSync(\"" + origCodeFileName + "\")) {\n\t\t\tvar gunzip = zlib_uniqID.gunzipSync;\n\t\t\tvar inp = fs_uniqID.createReadStream(\"" + origCodeFileName + ".gz\");\n\t\t\tvar out = fs_uniqID.createWriteStream(\"" + origCodeFileName + "\");\n\t\t\tinp.pipe(gunzip).pipe(out);\n\t\t}\n\t\tlet fileContents = fs_uniqID.readFileSync(\"" + origCodeFileName + "\", 'utf-8'); \n\t\tlet result_uniqID = eval(fileContents);";
    if (!esmMode) {
        body += "\nmodule.exports = result_uniqID;";
    }
    if (testingMode) {
        console.log("[STUBBIFIER METRICS] file stubbed: " + filename);
        body = "console.log(\"[STUBBIFIER METRICS] FILE STUB HAS BEEN EXPANDED: " + filename + "\");" + body;
    }
    //console.log((<babel.ExportNamedDeclaration> exportStmts.named[0]).specifiers)
    // create the exports:
    // for each named export, we need to create a variable declaration of the NE.specifiers[i].local.name
    // export NE.specifiers[i].local as NE.specifiers[i].exported
    var exportVars = "";
    var evalExports = "let evalRetVal = {";
    if (esmMode) {
        for (var _i = 0, _a = exportStmts.named; _i < _a.length; _i++) {
            var NE = _a[_i];
            for (var _b = 0, _c = NE.specifiers; _b < _c.length; _b++) {
                var spec = _c[_b];
                // TODO: Why is the type wrong here?
                if (spec.type == "ExportSpecifier") {
                    exportVars += "let " + spec.local.name + "_uniqID = result_uniqID[\"" + spec.local.name + "\"];";
                    evalExports += spec.local.name + " : " + generator_1["default"](spec.local).code + ", ";
                    spec.local.name += "_uniqID";
                }
            }
        }
        if (exportStmts["default"].length == 1) {
            exportVars += "export default result_uniqID[\"default\"];";
            evalExports += "default : " + generator_1["default"](exportStmts["default"][0].declaration).code;
        }
        evalExports += "}; evalRetVal;";
    }
    var outputAST = parser_1.parse(requires + body + exportVars, { sourceType: "unambiguous" }).program;
    if (esmMode) {
        // add import statements to the start of the stub, and exports to the end
        outputAST = core_1.transformFromAstSync(outputAST, null, { ast: true, plugins: [
                function visitAndAddImpExps() {
                    return {
                        visitor: {
                            Program: function (path) {
                                path.node.body = importStmts.concat(path.node.body);
                                for (var _i = 0, _a = Object.entries(exportStmts); _i < _a.length; _i++) {
                                    var _b = _a[_i], expKey = _b[0], expVal = _b[1];
                                    if (expKey != "default") {
                                        path.node.body = path.node.body.concat(expVal);
                                    }
                                }
                                path.skip();
                            }
                        }
                    };
                }
            ]
        }).ast;
        // add the evalRetVal to the end of the old code, so if it's loaded in 
        // the exports in the stub will work as expected
        ast = core_1.transformFromAstSync(ast, null, { ast: true, plugins: [
                function visitAndAddEvalExports() {
                    return {
                        visitor: {
                            Program: function (path) {
                                path.node.body = path.node.body.concat(parser_1.parse(evalExports, { sourceType: "unambiguous" }).program.body);
                                path.skip();
                            }
                        }
                    };
                }
            ]
        }).ast;
    }
    // write out stub, overwriting the original file
    // Debug: adding "help"
    fs.writeFileSync(filename, generator_1["default"](outputAST).code);
    // write out old code, post whatever processing is required
    var codeBodyOutput = generator_1["default"](ast).code;
    if (safeEvalMode) {
        codeBodyOutput = "let dangerousFunctions = [eval]; if( process){dangerousFunctions += [process.exec]}; dangerousFunctions += [require('child_process').execSync, require('child_process').exec];" + codeBodyOutput;
    }
    if (!esmMode) {
        codeBodyOutput += "\nmodule.exports;";
    }
    // were writing out the original code as-is.
    // fs.writeFileSync(origCodeFileName, codeBodyOutput);
    // instead write out a zipped version, to conserve space.
    if (zipFiles) {
        var gzip = zlib.createGzip();
        var out = fs.createWriteStream(origCodeFileName + '.gz');
        stream_1.Readable.from(codeBodyOutput).pipe(gzip).pipe(out);
    }
    else {
        fs.writeFileSync(origCodeFileName, codeBodyOutput);
    }
}
exports.fileStubFile = stubifyFile;
function stubifyDirectory(dirname, filesToRead, safeEvalMode, testingMode) {
    if (safeEvalMode === void 0) { safeEvalMode = false; }
    if (testingMode === void 0) { testingMode = false; }
    // check the package.json in the root of the directory (if it exists)
    // to check the type property (if it exists)
    // to see if this project uses ES6 modules (i.e. imports/exports)
    // default is that this is not the case 
    var esmMode = false;
    try {
        var json = JSON.parse(fs.readFileSync(dirname + "/package.json", 'utf-8'));
        esmMode = json.type == "module";
    }
    catch (e) { } // if there's an error, then we're not using esm
    // apply the transformer to each JS file in the list
    filesToRead.forEach(function (file, index) {
        // only stubify JS files
        var curPath = dirname + "/" + file;
        if (file.substr(file.length - 3) == ".js") {
            stubifyFile(curPath, safeEvalMode, testingMode);
        }
    });
}

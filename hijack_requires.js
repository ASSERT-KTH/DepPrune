const Module = require('module');

const originalRequire = Module.prototype.require;

Module.prototype.require = function hijacked(file) {
    console.log('Hijacked require:', file);
    // if (file == 'stop-iteration-iterator') {
    //     return function(){}
    // }
    // console.log('Hijacked require:', path.resolve(file));
    return originalRequire.apply(this, arguments);
}

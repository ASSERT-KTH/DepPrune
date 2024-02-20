const Module = require('module');
// const path = require('path')

const originalRequire = Module.prototype.require;

Module.prototype.require = function hijacked(file) {
    console.log('Hijacked require:', file);
    // console.log('Hijacked require:', path.resolve(file));
    return originalRequire.apply(this, arguments);
}

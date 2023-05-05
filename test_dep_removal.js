const protocol = require('./constants');
const { Buffer } = require('buffer');
const empty = Buffer.allocUnsafe(0);
const zeroBuf = Buffer.from([0])
const numbers = require('./numbers');
const nextTick = require('buffer').nextTick;
const debug = require('buffer')('mqtt-packet:writeToStream')

var Stream = require('./internal/streams/stream');

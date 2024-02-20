const { spawn } = require('node:child_process');
const path = require('path');

const test = spawn('npm', ['run', 'test'], {
  env: {
    ...process.env,
    NODE_OPTIONS: `--require ${path.join(__dirname, 'hijack_requires.js')}`
  }
});

test.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

test.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

// test.on('close', (code) => {
//   console.log(`Child process exited with code ${code}`);
// });

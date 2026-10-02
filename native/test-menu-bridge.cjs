const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = process.argv[2];
if (!root) throw new Error('Pass the prepared upstream directory');
const read = name => fs.readFileSync(path.join(root, 'frontend/autoloader/relapse/src', name), 'utf8');
const main = read('main.js');
const early = main.slice(main.indexOf('  if (await isElfldrListening'),
  main.indexOf('  const { runKernelExploit }'));
assert.ok(early.includes('await startAutoload(p, chain)'));
assert.ok(main.includes('kind: "menu-ready"'));
assert.ok(!read('webkit.js').includes('MAX_SAFE_ATTEMPTS'));
assert.ok(!read('site.js').includes('Restart the console before another attempt'));
(async () => {
  for (const running of [true, false]) {
    let menus = 0;
    let kernel = 0;
    await vm.runInNewContext('(async () => {' + early + '\nnext(); })()', {
      p:{}, chain:{}, log(){}, isElfldrListening:async () => running,
      startAutoload:async () => {menus++;}, next(){kernel++;}
    });
    assert.equal(menus, Number(running));
    assert.equal(kernel, Number(!running));
  }
  console.log('PASS: existing-loader menu branch retained; custom stability patches absent');
})().catch(error => {console.error(error); process.exitCode = 1;});

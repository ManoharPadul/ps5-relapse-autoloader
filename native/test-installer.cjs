const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(process.argv[2] + '/frontend/installer-page/index.html', 'utf8');
for (const m of source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)) new vm.Script(m[1]);
function extract(name, next) {
  const start = source.indexOf('      function ' + name + '(');
  const end = source.indexOf('      function ' + next + '(', start);
  assert.ok(start >= 0 && end > start);
  return source.slice(start,end);
}
const maybe = extract('maybeInstall','setCacheCorrupted');
for (const ready of [false,true]) for (const state of [0,1,2,3,4,5]) {
  let installed=0;
  const ctx={completed:false,probeOk:ready,cacheReady:false,isDownloading:state===3,
    window:{applicationCache:{status:state,IDLE:1,UPDATEREADY:4}},
    installApp(){installed++;}};
  vm.runInNewContext(maybe+'\nmaybeInstall(); maybeInstall();',ctx);
  assert.equal(installed,Number(ready && (state===1 || state===4)));
}
let installed=0;
const ctx={completed:false,probeOk:false,cacheReady:false,isDownloading:false,
  window:{applicationCache:{status:1,IDLE:1,UPDATEREADY:4}},installApp(){installed++;}};
vm.runInNewContext(maybe+'\nmaybeInstall();',ctx);
assert.equal(installed,0);
ctx.probeOk=true; ctx.maybeInstall(); assert.equal(installed,1);
let failures=0;
const failed={completed:false,detailEl:{},setFailed(){failures++;}};
// No window/location exists here: any navigation would fail this test.
vm.runInNewContext(extract('goToAutoloader','probeServer')+'\ngoToAutoloader(); goToAutoloader();',failed);
assert.equal(failures,1);
assert.match(failed.detailEl.textContent,/No jailbreak was started/);
assert.ok(source.includes('if (!probeOk) return; // Probe is asynchronous'));
console.log('PASS: cache/server readiness gate, event ordering, install once, no jailbreak navigation on probe failure');

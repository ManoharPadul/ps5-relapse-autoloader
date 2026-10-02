// Exercise control flow only: never run the memory primitive or kernel exploit.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = process.argv[2];
if (!root) throw new Error('Pass the prepared upstream directory');
const read = name => fs.readFileSync(path.join(root, 'frontend/autoloader', name), 'utf8');
const webkit = read('relapse/src/webkit.js');
const retry = webkit.slice(webkit.indexOf('function retry('), webkit.indexOf('function finishEarlySafeAttempt('));
for (const [attempt, safe, terminal] of [[1,true,false],[4,true,false],[5,true,true],[1,false,true]]) {
  const calls = {release:0, timers:0, rejected:0, starts:0};
  const context = { attemptNumber:attempt, MAX_SAFE_ATTEMPTS:5, Error,
    emit(){}, releaseAttempt(){ calls.release++; },
    settleReject(error){ assert.match(error.message, /Restart the console/); calls.rejected++; },
    setTimeout(fn, delay){ assert.equal(delay,750); calls.timers++; fn(); },
    startAttempt(){calls.starts++;} };
  vm.runInNewContext(retry + `\nretry('test failure', ${safe});`, context);
  assert.equal(calls.rejected, Number(terminal));
  assert.equal(calls.timers, Number(!terminal));
  assert.equal(calls.starts, Number(!terminal));
  assert.equal(calls.release, Number(safe));
}
const kernel = read('relapse/src/relapse_exploit.js');
assert.match(kernel, /done: false, payloads: false, error: why/);
const main = read('relapse/src/main.js');
assert.ok(!main.includes('kernel chain complete: root and sandbox escape are active'));
assert.ok(main.includes('(result && result.error)'));
const site = read('relapse/src/site.js');
const messages = [];
const failure = site.slice(site.indexOf('run().catch('));
vm.runInNewContext(failure, {Error, String, writeLog(){},
  run(){return {catch(fn){fn(new Error('armings did not complete'));}};},
  window:{parent:{postMessage(message){messages.push(message);}}} });
assert.equal(messages.length,1);
assert.equal(messages[0].ok,false);
assert.match(messages[0].why,/armings did not complete/);
assert.ok(!site.includes('kind: "log"'));
assert.ok(read('app.js').includes("(data.ok || exploitMode === 'relapse') && mirrorTimer"));
console.log('PASS: bounded safe retries, unsafe-state stop, kernel failure semantics, terminal error propagation');

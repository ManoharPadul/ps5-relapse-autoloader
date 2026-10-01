const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function boot(saved = '0') {
  const ids = {}, storage = { value: saved }, sent = [], requested = [];
  class Element {
    constructor() { this.children = []; this.style = {}; this.attributes = {}; }
    appendChild(el) { this.children.push(el); if (el.id) ids[el.id] = el; }
    setAttribute(k, v) { this.attributes[k] = v; }
    set src(value) { requested.push(value); }
    set innerHTML(value) {
      for (const m of value.matchAll(/id="([^"]+)"/g)) ids[m[1]] = new Element();
    }
  }
  const document = { body: new Element(), head: new Element(), createElement: () => new Element(), getElementById: id => ids[id] };
  const window = { PAYLOAD_TILES: [{ title: 'FTP', description: 'FTP server', name: 'ftpsrv-ps5.elf', key: 'ftp' }] };
  const context = { window, document, Promise, localStorage: {
    getItem: () => storage.value,
    setItem: (_, v) => { storage.value = v; }
  }};
  // No timer API is provided: a startup/autoload delay is a regression.
  vm.runInNewContext(fs.readFileSync(__dirname + '/payload-ui.js', 'utf8'), context);
  return { ids, storage, window, sent, requested, toggle: ids['relapse-options'].children[0],
    ready: () => window.RelapsePayloadUI.ready(name => { sent.push(name); return Promise.resolve(123); }) };
}
const settle = async () => { for (let i = 0; i < 8; i++) await Promise.resolve(); };
(async () => {
  const manual = boot();
  assert.equal(manual.ids['relapse-menu'], undefined);
  assert.equal(manual.requested.length, 0, 'No card assets requested before jailbreak');
  manual.toggle.onclick(); manual.toggle.onclick();
  assert.equal(manual.storage.value, '0');
  assert.equal(manual.toggle.attributes['aria-checked'], 'false');
  assert.equal(manual.sent.length, 0);
  manual.ready();
  assert.equal(manual.requested.length, 1, 'Card image requested only after readiness');
  assert.equal(manual.ids['relapse-menu'].style.display, 'block');
  assert.equal(manual.sent.length, 0);
  manual.ids['relapse-cards'].children[0].onclick();
  manual.ids['relapse-cards'].children[0].onclick();
  await settle();
  assert.deepEqual(manual.sent, ['ftpsrv-ps5.elf']);
  assert.equal(manual.toggle.disabled, false);
  const automatic = boot('1');
  assert.equal(automatic.sent.length, 0);
  automatic.ready(); automatic.ready();
  await settle();
  assert.deepEqual(automatic.sent, ['pldmgr_v0.5.2.elf']);
  assert.equal(automatic.ids['relapse-menu'].style.display, 'block');
  automatic.toggle.onclick();
  assert.equal(automatic.storage.value, '0');
  const failure = boot();
  failure.window.RelapsePayloadUI.ready(() => Promise.reject(new Error('send failed')));
  failure.ids['relapse-cards'].children[0].onclick();
  await settle();
  assert.match(failure.ids['relapse-menu-status'].textContent, /send failed/);
  assert.equal(failure.ids['relapse-cards'].children[0].disabled, false);
  console.log('PASS: readiness gate, immediate autoload, manual send, toggle persistence, duplicate-send guard, error recovery');
})().catch(error => { console.error(error); process.exitCode = 1; });

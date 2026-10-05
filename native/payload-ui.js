(function () {
  'use strict';
  var key = 'relapse-native-autoload-manager';
  var automatic = false, sender = null, busy = false;
  var tiles = window.PAYLOAD_TILES || [];
  var manager = 'pldmgr_v0.5.2.elf';
  try { automatic = localStorage.getItem(key) === '1'; } catch (e) {}
  var options = document.createElement('div');
  options.id = 'relapse-options';
  var toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.setAttribute('role', 'switch');
  options.appendChild(toggle);
  document.body.appendChild(options);
  var menu, status, cards;
  function buildMenu() {
  var sheet = document.createElement('link');
  sheet.rel = 'stylesheet'; sheet.href = 'payload-ui.css';
  document.head.appendChild(sheet);
  menu = document.createElement('section');
  menu.id = 'relapse-menu';
  menu.innerHTML = '<p class="credit">PS5 RELAPSE / PAYLOAD CENTER</p><h1>Payloads</h1>' +
    '<p>By Manohar Padul</p><p>Select a payload to send it to the local ELF loader.</p>' +
    '<p id="relapse-run-time"></p>' +
    '<p id="relapse-menu-status" role="status"></p><div id="relapse-cards"></div>';
  document.body.appendChild(menu);
  status = document.getElementById('relapse-menu-status');
  cards = document.getElementById('relapse-cards');
  tiles.forEach(function (tile) {
    var button = document.createElement('button');
    button.type = 'button';
    button.setAttribute('aria-label', tile.title + '. ' + tile.description);
    var fallback = document.createElement('span');
    fallback.className = 'fallback';
    var title = document.createElement('strong'); title.textContent = tile.title;
    var description = document.createElement('small'); description.textContent = tile.description;
    fallback.appendChild(title); fallback.appendChild(description);
    var art = document.createElement('img');
    art.alt = tile.title;
    art.onerror = function () { art.style.display = 'none'; fallback.style.display = 'block'; };
    if (tile.key === 'game-compressor') art.onerror();
    else art.src = 'ui/btn-' + tile.key + '-default.png';
    button.appendChild(art); button.appendChild(fallback);
    button.onclick = function () { send(tile.name); };
    cards.appendChild(button);
  });
  }
  function label() {
    toggle.textContent = 'Autoload Payload Manager: ' + (automatic ? 'ON' : 'OFF');
    toggle.setAttribute('aria-checked', automatic ? 'true' : 'false');
  }
  function showMenu() { menu.style.display = 'block'; }
  function report(message, failed) {
    status.textContent = message;
    if (window.uiLog) window.uiLog(message, failed ? 'error' : 'info');
  }
  function send(name) {
    if (!sender || busy) return;
    busy = true;
    toggle.disabled = true;
    for (var i = 0; i < cards.children.length; i++) cards.children[i].disabled = true;
    report('Sending ' + name + '...');
    Promise.resolve().then(function () { return sender(name); }).then(function (bytes) {
      report(name + ': sent ' + bytes + ' bytes.' + (name === manager ? ' Open http://PS5-IP:8084/ from another device.' : ''));
    }, function (error) {
      showMenu();
      report('Could not load ' + name + ': ' + (error.message || error), true);
    }).then(function () {
      busy = false;
      toggle.disabled = false;
      for (var i = 0; i < cards.children.length; i++) cards.children[i].disabled = false;
    });
  }
  toggle.onclick = function () {
    if (busy) return;
    automatic = !automatic;
    try { localStorage.setItem(key, automatic ? '1' : '0'); } catch (e) {}
    label();
    if (sender) {
      if (automatic) send(manager);
      else { showMenu(); report('ELF loader ready. Choose a payload.'); }
    }
  };
  label();
  window.RelapsePayloadUI = {
    ready: function (sendPayload) {
      if (sender || typeof sendPayload !== 'function') return;
      sender = sendPayload;
      buildMenu();
      if (window.__relapseChainStartedAt) {
        document.getElementById('relapse-run-time').textContent = 'Jailbreak completed in ' +
          ((Date.now() - window.__relapseChainStartedAt) / 1000).toFixed(1) + ' seconds.';
      }
      showMenu();
      if (automatic) send(manager);
      else { showMenu(); report('ELF loader ready. Choose a payload.'); }
    }
  };
})();

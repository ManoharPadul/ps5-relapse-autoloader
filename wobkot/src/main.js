const logger = {
  verbose: true, // enable for debug logs

  init() {
    this.console = document.getElementById('console');
  },
  info(msg) {
    this.log('[+]', `${msg}`);
  },
  error(msg) {
    this.log('[-]', `${msg}`);
  },
  debug(msg) {
    if (this.verbose) this.log('[*]', `${msg}`);
  },
  log(prefix, msg) {
    if (!this.console) return;

    const line = `${prefix} ${String(msg).replace(/\n/g, `\n${prefix} `)}`;
    this.console.append(`${line}\n`);
    this.console.scrollTop = this.console.scrollHeight;
    if (window.parent !== window) {
      window.parent.postMessage({ type: 'wkal', kind: 'log', message: line }, '*');
    }
  },
};

window.onerror = function (message, source, line, column, error) {
  let msg = message;

  if (error && error.stack) {
    msg += `\n${error.stack}`;
  } else {
    msg += `\n@${source}:${line}:${column}`;
  }

  logger.error(msg);
  if (window.parent !== window) {
    window.parent.postMessage({ type: 'wkal', kind: 'log', message: '[-] ' + msg }, '*');
  }
  return true;
};

window.onunhandledrejection = function (event) {
  const err = event.reason;

  let msg = err && err.message ? err.message : String(err);

  if (err && err.stack) {
    msg += `\n${err.stack}`;
  }

  logger.error(msg);
  if (window.parent !== window) {
    window.parent.postMessage({ type: 'wkal', kind: 'log', message: '[-] ' + msg }, '*');
  }
};

function load_script(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = resolve;
    script.onerror = () => {
      reject(new Error(`Failed to load script: ${src}`));
    };
    document.head.appendChild(script);
  });
}

async function load_file(src) {
  const res = await fetch(src);

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${src}`);
  }

  const buf = await res.arrayBuffer();
  return new Uint8Array(buf);
}

async function main() {
  window.__relapseChainStartedAt = Date.now();
  await load_script('src/misc.js');

  version.init();
  if (version.major < 7 || version.major > 13 ||
      (version.major === 13 && version.minor > 0x60)) {
    throw new Error(`Unsupported Wobkot firmware ${version}`);
  }
  const symbolTableFirmwares = new Set([
    '7.00', '7.01', '7.20', '7.40', '7.60', '7.61',
    '8.00', '8.20', '8.40', '8.60',
    '9.00', '9.20', '9.40', '9.60',
    '10.00', '10.01', '10.20', '10.40',
    '11.00', '11.20', '11.60',
    '12.00', '12.02', '12.20', '12.40', '12.60', '12.70',
    '13.00', '13.20', '13.40', '13.42', '13.60',
  ]);
  if (symbolTableFirmwares.has(version.toString())) {
    await load_script(`../offsets/${version.toString()}.js`);
  } else {
    logger.debug(`No static Relapse symbol table for ${version}; resolving symbols from loaded modules`);
  }

  switch (version.console) {
    case 5:
      await load_script('src/ps5/impl.js');
      break;
    default:
      throw new Error(`Wobkot PS5 route does not support console ${version.console}`);
  }

  await load_script('src/userland.js');
  await userland_main();

  await load_script('src/kernel.js');
  await kernel_main();

  window.__relapseSendPayload = async function (filename) {
    const allowed = (window.PAYLOAD_TILES || []).some((tile) => tile.name === filename);
    if (!allowed) throw new Error(`Unknown payload: ${filename}`);

    const payload = await load_file(`../payloads/${encodeURIComponent(filename)}`);
    if (payload.length < 4 || payload[0] !== 0x7f || payload[1] !== 0x45 ||
        payload[2] !== 0x4c || payload[3] !== 0x46) {
      throw new Error(`${filename} is not a valid ELF`);
    }

    const [payloadBuffer, payloadAddress] = mem.alloc(payload.length, true);
    const [addressBuffer, addressAddress] = mem.alloc(16, true);
    const addressView = new DataView(addressBuffer);
    addressView.setUint8(0, 16);
    addressView.setUint8(1, AF_INET);
    addressView.setUint8(2, 0x23);
    addressView.setUint8(3, 0x3d);
    addressView.setUint8(4, 127);
    addressView.setUint8(7, 1);
    mem.copy(payloadAddress, payload.buffer.data(), payload.length);

    const socket = fn.socket.invoke(AF_INET, SOCK_STREAM, 0);
    if (socket < 0) throw new SyscallError('Unable to create payload socket');

    try {
      if (fn.connect.invoke(socket, addressAddress, 16) === -1) {
        throw new SyscallError('elfldr is not listening on 127.0.0.1:9021');
      }

      let sent = 0;
      while (sent < payload.length) {
        const result = fn.write.invoke(socket, payloadAddress.add(sent), payload.length - sent);
        if (result.eq(-1) || result.lo === 0) {
          throw new SyscallError(`Payload send stopped after ${sent} bytes`);
        }
        sent += result.lo;
      }
      return sent;
    } finally {
      fn.close.invoke(socket);
      mem.allocs.delete(payloadBuffer);
      mem.allocs.delete(addressBuffer);
      payloadBuffer.free();
      addressBuffer.free();
    }
  };

  if (window.parent === window) {
    await load_script('payload-ui.js');
    window.RelapsePayloadUI.ready(window.__relapseSendPayload);
  } else {
    window.parent.postMessage({ type: 'wkal', kind: 'menu-ready' }, '*');
  }
}

logger.init();
main();

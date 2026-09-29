const CACHE_NAME = "ps5-offline-v24";
const OFFLINE_MARKER = "./__offline_ready_v24";

const STATIC_ASSETS = [
  "./",
  "./index.html",
  "./payloads.js",
  "./elf.html",
  "./firmware.js",
  "./main.js",
  "./core.js",
  "./mem.js",
  "./exploit.js",
  "./kexp.js",
  "./int64.js",
  "./rop.js",
  "./rop_slave.js",
  "./syscalls.js",
  "./offsets/7.00.js",
  "./offsets/7.01.js",
  "./offsets/7.20.js",
  "./offsets/7.40.js",
  "./offsets/7.60.js",
  "./offsets/7.61.js",
  "./offsets/8.00.js",
  "./offsets/8.20.js",
  "./offsets/8.40.js",
  "./offsets/8.60.js",
  "./offsets/9.00.js",
  "./offsets/9.20.js",
  "./offsets/9.40.js",
  "./offsets/9.60.js",
  "./offsets/10.00.js",
  "./offsets/10.01.js",
  "./offsets/10.20.js",
  "./offsets/10.40.js",
  "./offsets/11.00.js",
  "./offsets/11.20.js",
  "./offsets/11.60.js",
  "./offsets/12.00.js",
  "./offsets/12.02.js",
  "./offsets/12.20.js",
  "./offsets/12.40.js",
  "./offsets/12.60.js",
  "./offsets/12.70.js",
  "./offsets/13.00.js",
  "./offsets/13.20.js",
  "./offsets/13.40.js",
  "./offsets/13.42.js",
  "./offsets/13.60.js",
  "./ui/btn-etahen-default.png",
  "./ui/btn-etahen-failed.png",
  "./ui/btn-etahen-sending.png",
  "./ui/btn-etahen-sent.png",
  "./ui/btn-ftp-default.png",
  "./ui/btn-ftp-failed.png",
  "./ui/btn-ftp-sending.png",
  "./ui/btn-ftp-sent.png",
  "./ui/btn-klog-default.png",
  "./ui/btn-klog-failed.png",
  "./ui/btn-klog-sending.png",
  "./ui/btn-klog-sent.png",
  "./ui/btn-kstuff-default.png",
  "./ui/btn-kstuff-failed.png",
  "./ui/btn-kstuff-sending.png",
  "./ui/btn-kstuff-sent.png",
  "./ui/btn-web-default.png",
  "./ui/btn-web-failed.png",
  "./ui/btn-web-sending.png",
  "./ui/btn-web-sent.png",
  "./ui/hdr-payloads.png"
];

/* The install event stays small so registering a new worker never competes
   with the exploit. The page explicitly asks for this complete bundle and
   waits for the marker before starting the jailbreak. */
const OFFLINE_PAYLOADS = [
  "./payloads/elfldr-ps5-1360.elf",
  "./payloads/etaHEN.elf",
  "./payloads/ftpsrv-ps5.elf",
  "./payloads/game-compressor.elf",
  "./payloads/kexp_2026_05_25.bin",
  "./payloads/kstuff.elf",
  "./payloads/nanodns.elf",
  "./payloads/pldmgr_v0.5.2.elf",
  "./payloads/shadowmountplus.elf",
  "./payloads/websrv-ps5.elf"
];
const OFFLINE_ASSETS = STATIC_ASSETS.concat(OFFLINE_PAYLOADS);

function reply(event, message) {
  const port = event.ports && event.ports[0];
  if (port) port.postMessage(message);
  else if (event.source) event.source.postMessage(message);
}

self.addEventListener("message", function (event) {
  const data = event.data || {};
  if (data.type === "offline-version") {
    reply(event, { type: "offline-version", cache: CACHE_NAME });
    return;
  }
  if (data.type !== "prepare-offline") return;

  const task = (async function () {
    const cache = await caches.open(CACHE_NAME);
    if (await cache.match(OFFLINE_MARKER)) {
      reply(event, { type: "offline-ready", cached: true });
      return;
    }

    for (let i = 0; i < OFFLINE_ASSETS.length; i++) {
      const asset = OFFLINE_ASSETS[i];
      const request = new Request(asset, { cache: "no-store" });
      let response = await cache.match(request, { ignoreSearch: true });
      if (!response) {
        response = await fetch(request);
        if (!response.ok) throw new Error(asset + " -> HTTP " + response.status);
        await cache.put(request, response.clone());
      }
      reply(event, {
        type: "offline-progress",
        done: i + 1,
        total: OFFLINE_ASSETS.length,
        asset: asset
      });
    }

    await cache.put(
      OFFLINE_MARKER,
      new Response(CACHE_NAME, { headers: { "Content-Type": "text/plain" } }),
    );
    reply(event, { type: "offline-ready", cached: false });
  })();

  event.waitUntil(task.catch(function (error) {
    reply(event, {
      type: "offline-error",
      error: String((error && error.message) || error)
    });
  }));
});

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) { return cache.addAll(STATIC_ASSETS); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys
        .filter(function (key) { return key !== CACHE_NAME; })
        .map(function (key) { return caches.delete(key); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (request.method !== "GET") return;

  var url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.indexOf("/api/") !== -1 || url.pathname.indexOf("/log/") !== -1) return;

  var refreshOnline = request.mode === "navigate"
    || /\/(?:payloads|sw)\.js$/.test(url.pathname);
  var fromNetwork = function () {
    return fetch(request, { cache: "no-store" }).then(function (response) {
      if (response.ok && response.type === "basic") {
        caches.open(CACHE_NAME).then(function (cache) {
          cache.put(request, response.clone());
        });
      }
      return response;
    });
  };
  var fromCache = function () {
    return caches.match(request, { ignoreSearch: true });
  };

  event.respondWith(
    (refreshOnline ? fromNetwork().catch(fromCache) : fromCache().then(function (cached) {
      return cached || fromNetwork();
    })).catch(function () {
      if (request.mode === "navigate") {
        return caches.match("./index.html", { ignoreSearch: true });
      }
      return Response.error();
    })
  );
});

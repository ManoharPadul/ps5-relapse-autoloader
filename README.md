# relapse

PS5 WebKit + kernel exploit chain (relapse / aio), firmware **7.00 - 13.60**.

Retail and testkit build. Devkits want the [relapse-dev](https://github.com/soniciso1/relapse-dev) build instead.

Open the page on the console. It first prepares and verifies the complete offline
cache, then starts the jailbreak. A successful run draws the payload menu in place
and sends each ELF through the console's own syscalls to `127.0.0.1:9021`, so no
server-side support is needed and this works from any static host.

Supported: 7.00, 7.01, 7.20, 7.40, 7.60, 7.61, 8.00, 8.20, 8.40, 8.60, 9.00, 9.20,
9.40, 9.60, 10.00, 10.01, 10.20, 10.40, 11.00, 11.20, 11.60, 12.00, 12.02, 12.20,
12.40, 12.60, 12.70, 13.00, 13.20, 13.40, 13.42, 13.60.

10.60 and 11.40 are absent: those firmware images are missing the modules the offsets
have to be read out of.

`elf.html` is a standalone payload menu for the already-jailbroken case. It needs a
host that runs code and can reach the console (`api/` ships PHP and node handlers),
so it does not work on GitHub Pages - use the run page's own menu there.

## Offline browser cache

The first visit must be online. The page downloads the static files and payloads
sequentially, writes an offline-ready marker only after every file succeeds, and
starts the exploit only after that marker exists. Later visits use the completed
cache before running the exploit. If the first cache pass is interrupted, the
exploit is not started and the next online visit resumes the preparation.

Clearing PS5 browser data removes the cache and requires one more online visit.

The published site is `https://manoharpadul.github.io/relapse/`.

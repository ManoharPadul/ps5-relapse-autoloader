# PS5 Relapse AutoLoader v0.2.0 — Offline Release Notes

## Offline networking requirement

After the complete Relapse cache has been installed, Internet/WAN access is not
required. The PS5 must still remain connected to Wi-Fi or Ethernet/LAN and must
have a valid local IPv4 address.

Check:

**Settings → Network → View Connection Status → Obtain IP Address**

The result must be successful. Typical addresses are:

```text
192.168.1.x       home router
172.20.10.x       iPhone Personal Hotspot
10.x.x.x          private LAN
```

`127.0.0.1`, an empty address, or `0.0.0.0` does not count. `127.0.0.1` is the
PS5's loopback address only. The 13.60 jailbreak route/KASLR step needs a real
local interface, even when the local network has no Internet connection.

An iPhone hotspot may be used without Internet only when it still assigns the
PS5 a local address through DHCP. If cellular data is disabled and the PS5 gets
no address, use a DHCP-enabled router/access point with WAN disconnected.

## v0.2.0 changes

- Added an explicit local Wi-Fi/LAN interface check for the 13.60 route step.
- Removed the unsafe loopback fallback.
- Added a short wait for Wi-Fi/LAN DHCP initialization.
- Improved offline-cache and payload-menu behavior.
- Preserved the bundled payload menu and optional PLK Manager autoload.

## Installation

1. Complete the initial cache installation while online.
2. Connect the PS5 to Wi-Fi/LAN and confirm it has a local IP address.
3. Start the supported jailbreak chain and `elfldr` on port `9021`.
4. Send:

```text
ps5-relapse-autoloader-installer.0.2.0.elf
```

5. Allow the cache/application installation to finish.
6. Later sessions can run without Internet, but Wi-Fi/LAN and a local IP remain
   required.

## Release files

```text
ps5-relapse-autoloader-installer.0.2.0.elf
ps5-relapse-autoloader-installer.0.2.0.elf.sha256
```

SHA-256:

```text
5EA5DE3CFF602DEC1830ED77487CBFD0A177F0DA014AD310947D07121EF7F2E8
```

Builds must be tested on the target PS5 before being considered fully verified.


# PS5 Relapse AutoLoader v0.2.0

## Overview

PS5 Relapse AutoLoader v0.2.0 is a native Relapse installer and offline-first
jailbreak frontend for PS5 firmware **7.00–13.60**.

This release improves PS5 WebKit payload-menu rendering, offline-cache startup,
payload delivery, PLK Manager autoload, and local Wi-Fi/LAN handling.

## Important: a local IP address is required

Internet access is not required after the complete cache has been installed, but
the PS5 must remain connected to Wi-Fi or Ethernet/LAN and receive a valid local
IPv4 address.

Check:

**Settings → Network → View Connection Status → Obtain IP Address**

The result must be successful. Examples:

```text
192.168.1.x       home router or access point
172.20.10.x       common iPhone Personal Hotspot range
10.x.x.x          private LAN range
```

`127.0.0.1`, a blank address, or `0.0.0.0` does not count. `127.0.0.1` is
only the PS5's loopback address. The 13.60 route-based KASLR step requires a
real local Wi-Fi/LAN interface, even when the local network has no Internet.

An iPhone hotspot can work without Internet only if it still assigns the PS5 a
local address through DHCP. If disabling cellular data leaves the PS5 without
an IP address, use a DHCP-enabled router or access point with WAN disconnected.

## What's new in v0.2.0

### Payload menu

- Improved PS5 WebKit payload-card rendering.
- Reduced dependence on hover or focus events for card visibility.
- Improved controller-friendly buttons and payload layout.
- Improved transition after `elfldr` becomes available.
- Kept the payload menu inside the active exploit session.

### Offline cache

- Improved cache preparation before starting the jailbreak.
- Bundled scripts, firmware offsets, UI assets, and payloads are staged locally.
- Cached files can be used without Internet after initial preparation.
- A new versioned cache is generated for v0.2.0.

### Network and 13.60 stability

- Removed the unsafe loopback fallback from the 13.60 KASLR route step.
- Added a short wait for Wi-Fi/LAN DHCP initialization.
- Reports a clear local-interface error when the PS5 has no usable IP address.

### PLK Manager autoload

When enabled, Relapse:

1. Completes the jailbreak.
2. Waits five seconds after `elfldr` is ready.
3. Sends `pldmgr_v0.5.2.elf` to port `9021`.
4. Opens:

```text
http://<PS5-IP>:8084/
```

When disabled, the normal payload menu opens.

## Included payloads

| Payload | Port or service |
|---|---:|
| ELF loader | 9021 |
| etaHEN | 9021 |
| ps5-kstuff | 9021 |
| ftpsrv | 2121 |
| websrv | 8080 |
| PLK Manager v0.5.2 | 8084 |
| nanodns | 9021 |
| shadowmountplus | 9021 |
| Game Compressor 1.0.4 | 5910 |

`127.0.0.1:9021` refers to the PS5 itself. From another device, use the PS5's
local IP address, for example `http://192.168.1.103:8084/`.

## Requirements

- Supported firmware: **7.00–13.60**.
- A valid local PS5 Wi-Fi/LAN IPv4 address.
- `elfldr` running on `127.0.0.1:9021` for native ELF installation.
- The installer ELF sent through an existing payload loader.
- The native installer requires an already-jailbroken PS5; it is not a
  standalone jailbreak for a clean console.

Firmware 10.60 and 11.40 are not included because the required module offsets
are unavailable.

## Installation and updating

1. While online, install the AutoLoader and wait for the complete cache to
   finish.
2. Connect the PS5 to Wi-Fi or Ethernet/LAN and confirm it has a local IP.
3. Start the supported jailbreak chain and `elfldr` on port `9021`.
4. Send:

```text
ps5-relapse-autoloader-installer.0.2.0.elf
```

5. Allow the application and cache installation to finish.
6. Launch **PS5 Relapse AutoLoader** from the PS5 Media section.

After caching, WAN Internet can be disabled. Do not disable the PS5's local
Wi-Fi/LAN connection.

## Release files

```text
ps5-relapse-autoloader-installer.0.2.0.elf
ps5-relapse-autoloader-installer.0.2.0.elf.sha256
```

SHA-256:

```text
5EA5DE3CFF602DEC1830ED77487CBFD0A177F0DA014AD310947D07121EF7F2E8
```

## Disclaimer

Use this project only on hardware you own or are authorized to test. A
successful build does not guarantee identical behavior on every console or
network configuration. Test the ELF on the target PS5 before treating it as
fully verified.

## Credits

Based on the original Relapse project, PS5 WebKit/kernel exploit work, PS5
payload SDK, `elfldr`, and open-source PS5 payload projects. Native installer
integration, offline caching, payload-menu work, network handling, and Relapse
branding by **Manohar Padul**.


# PS5 Relapse AutoLoader v0.1.0

## Overview

PS5 Relapse AutoLoader is a native ELF installer for the Relapse PS5 WebKit/kernel exploit frontend. It installs a cached Relapse application on the PS5 and provides an offline-first way to launch the jailbreak page and payload menu.

This release includes the Relapse frontend with firmware support up to **13.60**, offline caching, payload support, custom Relapse branding, and the circular Relapse icon.

## Requirements

- PS5 firmware supported by Relapse: **7.00–13.60**
- An already-jailbroken PS5
- `elfldr` running on port `9021`
- The installer ELF sent through the PS5 ELF loader
- The installer does not jailbreak a clean PS5 by itself

## Installation

1. Jailbreak the PS5 normally.
2. Start `elfldr` and confirm it is listening on:

   ```text
   127.0.0.1:9021
   ```

3. Send this ELF through the payload menu:

   ```text
   ps5-relapse-autoloader-installer.0.1.elf
   ```

4. The installer starts a temporary local HTTP server.
5. It copies the Relapse browser files, firmware offsets, scripts, payloads, icons, and cache manifest.
6. It creates the PS5 Relapse AutoLoader homescreen application.
7. Launch **PS5 Relapse AutoLoader** from the PS5 Media section.

The installer is only required during the initial installation. After installation, the Relapse application uses its local cached bundle.

## Online and offline use

The first installation and cache preparation require internet access so the PS5 can download and store the complete Relapse bundle.

After the cache reports that it is ready:

- Internet access can be disabled.
- Keep the PS5 connected to Wi‑Fi or Ethernet/LAN.
- Keep the PS5 and other devices on the same local network.
- Completely disabling Wi‑Fi and disconnecting LAN may cause network-interface or KASLR errors.
- Clearing PS5 browser or application data removes the cache and requires another online setup.

```text
Internet: required for the first setup and online downloads
Wi‑Fi/LAN: recommended for every jailbreak session
Internet after caching: not required
```

The installed native application does not need GitHub Pages to remain available after the cache has been installed.

## Payload workflow

After a successful jailbreak, Relapse keeps the exploit page active and opens the payload menu. Payloads are sent locally through `elfldr` on port `9021`.

| Payload | Port |
|---|---:|
| ELF loader | 9021 |
| PLK Manager v0.5.2 | 8084 |
| Game Compressor 1.0.4 | 5910 |
| etaHEN | 9021 |
| kstuff | 9021 |
| ftpsrv | 2121 |
| websrv | 8080 |
| nanodns | 9021 |
| shadowmountplus | 9021 |

`127.0.0.1` refers to the PS5 itself. From another device, use the PS5's local IP address:

```text
http://<PS5-IP>:8084/
```

## PLK Manager autoload

Relapse includes an optional PLK Manager autoload toggle.

When enabled:

1. Relapse waits five seconds after a successful jailbreak.
2. It sends `pldmgr_v0.5.2.elf` to the local ELF loader.
3. It waits briefly for the service to start.
4. It opens:

   ```text
   http://<PS5-IP>:8084/
   ```

When disabled, the normal payload menu opens.

## Release files

```text
ps5-relapse-autoloader-installer.0.1.elf
ps5-relapse-autoloader-installer.0.1.elf.sha256
```

SHA-256:

```text
26B7D65F19EC465FCC60C61508B618476DD9D81280156FDFC843A6AEE0476367
```

The installer must be tested on the target PS5 firmware before being considered fully verified. A successful build confirms that the ELF is linked correctly, but does not guarantee that every payload works on every console configuration.

## Credits

Built from the original Relapse project and open-source PS5 payload projects, with additional offline caching, native installer integration, payload menu updates, 13.60 support work, and Relapse branding by **Manohar Padul**.

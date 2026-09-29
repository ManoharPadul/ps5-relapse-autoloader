<p align="center">
  <img src="./assets/icon.png" width="128" alt="PS5 Relapse icon" />
</p>

<h1 align="center">PS5 Relapse Autoloader</h1>

<p align="center">
  Offline-first WebKit and kernel-jailbreak frontend with an in-page ELF payload menu.<br />
  Supports Relapse firmware <b>7.00–13.60</b>.
</p>

Relapse AutoLoader v0.1.0 installs a cached Relapse application on the PS5. The
native installer is an installation and cache tool; it does **not** jailbreak a
clean PS5 by itself. The PS5 must already be jailbroken and have `elfldr` running.

<!-- Add console screenshots here later.
<p align="center">
  <img src="./.github/screenshots/relapse-jailbreak.jpg" width="260" alt="Relapse jailbreak screen" />
  <img src="./.github/screenshots/relapse-payloads.jpg" width="260" alt="Relapse payload menu" />
  <img src="./.github/screenshots/relapse-pldmgr.jpg" width="260" alt="Relapse Payload Manager" />
</p>
-->

## What it does

PS5 browser exploit pages normally depend on a remote host or DNS service. Relapse
stages its complete browser bundle locally first: the page verifies the scripts,
firmware offsets, exploit files, and payload ELFs before starting the jailbreak.
Once the cache is complete, the same page can be opened again without downloading
the bundle from the internet.

After elfldr is ready, Relapse keeps the exploit document alive and displays the
payload menu in place. Each payload is sent through the console-side loader on
`127.0.0.1:9021`, so the public static page does not need a server-side socket.

## Requirements

- PS5 firmware supported by the Relapse frontend: **7.00–13.60**.
- A PS5 that is already jailbroken for the native installer step.
- `elfldr` listening on console port `9021`.
- Wi-Fi or Ethernet/LAN enabled on the PS5 during jailbreak sessions.

## Current browser setup

1. Open the published page while the PS5 has internet access:
   [manoharpadul.github.io/relapse](https://manoharpadul.github.io/relapse/).
2. Let the **v20** offline-cache step finish. Do not close the browser during this
   first preparation pass.
3. Run the jailbreak. If elfldr is already running, Relapse opens the payload
   path without repeating the kernel chain.
4. On later runs, open the same bookmarked page. The completed cache is used first.

Clearing PS5 browser data removes the cache and requires one more online visit.

## pldmgr autoload

The boot-options card contains a persistent `Autoload pldmgr v0.5.2` toggle.
When enabled, Relapse waits five seconds after elfldr is ready, sends the official
13.60-compatible `payloads/pldmgr_v0.5.2.elf`, waits briefly for port 8084, and
opens `http://<console-ip>:8084/`. When disabled, the normal in-page payload menu
opens instead.

## Network use

The first installation and cache preparation need internet access. After the page
reports that the offline cache is ready, internet access can be disabled, but keep
the PS5 connected to the same local Wi-Fi/LAN as the device used to access its
services.

| Connection | Needed for |
|---|---|
| Internet/WAN | First cache setup and online downloads |
| Wi-Fi or Ethernet/LAN | Local PS5 networking and normal jailbreak sessions |
| Internet after caching | Not required |

Completely disabling Wi-Fi and disconnecting LAN may cause `kaslr: no configured
interface` or routing failures on some 13.60 runs. If PS5 browser data is cleared,
the cache must be prepared again while online.

## Payloads

The menu includes the bundled Relapse-compatible payloads. Payloads are sent to
the local ELF loader on port `9021`.

| Payload | Service port |
|---|---:|
| etaHEN | 9021 |
| ps5-kstuff | 9021 |
| ftpsrv | 2121 |
| websrv | 8080 |
| PLK Manager v0.5.2 | 8084 |
| nanodns | 9021 |
| shadowmountplus | 9021 |
| Game Compressor 1.0.4 | 5910 |

Game Compressor is rebuilt with the Relapse PS5 SDK for the 13.60 payload set.
PLK Manager v0.5.2 is included; the obsolete v0.5.1 binary is not included.

`127.0.0.1` refers to the PS5 itself. From another device, use the PS5's local
IP address, for example `http://<PS5-IP>:8084/` for PLK Manager.

## Firmware coverage

Supported firmware offsets currently include:

`7.00`, `7.01`, `7.20`, `7.40`, `7.60`, `7.61`, `8.00`, `8.20`, `8.40`, `8.60`,
`9.00`, `9.20`, `9.40`, `9.60`, `10.00`, `10.01`, `10.20`, `10.40`, `11.00`,
`11.20`, `11.60`, `12.00`, `12.02`, `12.20`, `12.40`, `12.60`, `12.70`, `13.00`,
`13.20`, `13.40`, `13.42`, and `13.60`.

Firmware 10.60 and 11.40 are not included because the required module offsets are
not available in those firmware images.

## Native offline installer

The separate native-ELF phase is documented in [`native/`](native/). It reuses the
upstream installer/build machinery while replacing the staged application with
the 13.60 Relapse frontend and payload bundle. The build also embeds the supplied
portrait as the PS5 homescreen icon.

The v0.1.0 installer is named:

```text
ps5-relapse-autoloader-installer.0.1.elf
```

Installation flow:

1. Jailbreak the PS5 and start `elfldr` on `127.0.0.1:9021`.
2. Send the installer ELF through the existing payload menu.
3. Let the temporary local installer server stage the cache and create the
   homescreen application.
4. Launch **PS5 Relapse AutoLoader** from the PS5 Media section.

The complete release text is in
[`RELEASE_NOTES_v0.1.0.md`](RELEASE_NOTES_v0.1.0.md). The native ELF must be tested
on the target PS5 before release; a successful compiler build does not guarantee
that every payload or firmware configuration will work.

The official upstream autoloader README documents a different firmware range,
ending at 12.70; its native installer is therefore treated here as generic cache
and homescreen-installation machinery, not as the 13.60 exploit chain. The native
ELF must be built and then tested on the target 13.60 console before release.

## Screenshots

Screenshots are intentionally left as placeholders above. Add them later under
`.github/screenshots/` without changing the build or cache logic.

## Developer notes

- `index.html` owns the cache-first gate, jailbreak flow, payload menu, and pldmgr
  toggle.
- `sw.js` downloads the offline bundle sequentially and writes the v20 marker only
  after the full bundle succeeds.
- `.github/workflows/native-installer.yml` builds the native installer with the
  official PS5 SDK container definition.

## Credits

Relapse builds on the PS5 WebKit/kernel exploit work, PS5 payload SDK, elfldr,
payload projects, and the open-source native installer architecture referenced in
the project sources. See the individual source files and linked upstream projects
for their respective licenses and contributors.

## Disclaimer

This project is provided as-is for research and development. Use it only on
hardware and software you own or are authorized to test. The authors are not
responsible for damage, data loss, or other consequences from its use.

## License

This repository remains under the license included with the project sources.

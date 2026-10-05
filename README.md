<p align="center">
  <img src="./assets/icon.png" width="128" alt="PS5 Relapse icon" />
</p>

<h1 align="center">PS5 Relapse Autoloader</h1>

<p align="center">
  Native offline AutoLoader with automatic payload loading, by Manohar Padul.<br />
  Supports Relapse firmware <b>7.00–13.60</b>.
</p>

Relapse AutoLoader v0.3.1 installs a cached Relapse application on the PS5. The
native installer is an installation and cache tool; it does **not** jailbreak a
clean PS5 by itself. The PS5 must already be jailbroken and have `elfldr` running.

<!-- Add console screenshots here later.
<p align="center">
  <img src="./.github/screenshots/relapse-jailbreak.jpg" width="260" alt="Relapse jailbreak screen" />
  <img src="./.github/screenshots/relapse-payloads.jpg" width="260" alt="Relapse payload menu" />
  <img src="./.github/screenshots/relapse-pldmgr.jpg" width="260" alt="Relapse Payload Manager" />
</p>
-->

For the current native ELF behavior and installation instructions, see
[v0.3.1 release notes](RELEASE_NOTES_v0.3.1.md) and [native build documentation](native/README.md).
The browser-hosted frontend described below is retained separately; its legacy
timers and menu implementation are not used by the v0.3.1 native build.

## Browser-hosted frontend

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
2. Let the **v21** offline-cache step finish. Do not close the browser during this
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

### A local IP address is required for the jailbreak

The PS5 must receive an IPv4 address from the Wi-Fi access point or Ethernet
router before starting the jailbreak. Check **Settings > Network > View Connection
Status** and confirm that **Obtain IP Address** is successful. Examples are
`192.168.1.x` on a home router or commonly `172.20.10.x` on an iPhone hotspot.

The internet connection itself is not required. A router with its WAN/internet
disconnected is fine as long as DHCP still gives the PS5 a local IP address. An
iPhone hotspot with cellular data disabled may fail to provide a usable local
interface, depending on the carrier and iPhone state. `127.0.0.1` is only PS5
loopback and does not count as the required Wi-Fi/LAN address.

| Connection | Needed for |
|---|---|
| Internet/WAN | First cache setup and online downloads |
| Wi-Fi or Ethernet/LAN with a local IP address | Local PS5 networking and normal jailbreak sessions |
| Internet after caching | Not required |

Internet after caching is not required, but the PS5 must still be associated with a
router or hotspot and receive a local IPv4 address such as `192.168.x.x`. The
exploit uses the PS5 route table for its 13.60 KASLR step; `127.0.0.1` loopback is
not sufficient. If the network test reports no IP address, use a DHCP-enabled
router/hotspot or Ethernet connection, even if that network has no WAN internet.
If PS5 browser data is cleared, the cache must be prepared again while online.

If the address is blank, `0.0.0.0`, or the exploit reports `no local IPv4
interface`, reconnect the PS5 to a DHCP-enabled Wi-Fi/LAN and retry. The cached
browser files can be offline, but the jailbreak still needs the local network
interface.

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

The v0.3.1 native build is documented in [`native/`](native/). It uses the
**itsPLK/ps5-webkit-autoloader v0.5.2** installer and automatic payload interface,
branded **PS5 Relapse AutoLoader — by Manohar Padul**, with the supplied circular
portrait. The installer and progress UI follow upstream. After a successful
Relapse jailbreak, **Autoload Payload Manager OFF** shows the Relapse payload
menu; **ON** immediately loads the bundled Payload Manager. The choice persists
across launches. There is no added startup or autoload delay in this ELF.

The Relapse menu is rendered in the outer UI document while its exploit iframe
stays alive to send payloads. Other upstream exploit routes keep their unified
autoload behavior. Configure subsequent autoloads through Payload Manager.

The v0.3.1 installer is named:

```text
ps5-relapse-autoloader-installer.0.3.1.elf
```

Installation flow:

1. Jailbreak the PS5 and start `elfldr` on `127.0.0.1:9021`.
2. Send the installer ELF through the existing payload menu.
3. Let the temporary local installer server stage the cache and create the
   homescreen application.
4. Reboot once, then launch **PS5 Relapse AutoLoader** from the PS5 Media section.

The complete release text is in
[`RELEASE_NOTES_v0.3.1.md`](RELEASE_NOTES_v0.3.1.md). The native ELF must be tested
on the target PS5 before release; a successful compiler build does not guarantee
that every payload or firmware configuration will work.

Upstream v0.5.2 includes firmware routing through 13.60. On 13.60 a usable local
Wi-Fi/Ethernet IP is required, even with the full offline cache. Each development
build uses a fresh timestamped content/cache version. Install the new ELF and
allow caching to finish before testing the new interface.

## Screenshots

Screenshots are intentionally left as placeholders above. Add them later under
`.github/screenshots/` without changing the build or cache logic.

## Developer notes

- `index.html` owns the cache-first gate, jailbreak flow, payload menu, and pldmgr
  toggle.
- `sw.js` downloads the offline bundle sequentially and writes the v21 marker only
  after the full bundle succeeds.
- `.github/workflows/native-installer.yml` builds the native installer with the
  official PS5 SDK container definition.

## Upstream projects and payload sources

This project is a Relapse-based integration and uses or references the following
open-source projects. Each upstream project retains its own license and credits.

| Project | Role in this project |
|---|---|
| [soniciso1/relapse](https://github.com/soniciso1/relapse) | Original Relapse PS5 WebKit/kernel exploit frontend and firmware-chain lineage |
| [itsPLK/ps5-webkit-autoloader](https://github.com/itsPLK/ps5-webkit-autoloader) | Native ELF installer, cache staging, homescreen installation, and build architecture |
| [itsPLK/ps5-payload-manager](https://github.com/itsPLK/ps5-payload-manager) | PLK Manager dashboard/payload source and port-8084 service workflow |
| [EchoStretch/kstuff-lite](https://github.com/EchoStretch/kstuff-lite) | `ps5-kstuff` payload source |
| [juma-sayeh/PS5-Game-Compressor](https://github.com/juma-sayeh/PS5-Game-Compressor) | Game Compressor payload source and service workflow |
| [etaHEN/etaHEN](https://github.com/etaHEN/etaHEN) | etaHEN AIO payload source |

The Relapse-specific additions include the offline-first cache flow, 13.60
frontend integration, local Wi-Fi/LAN interface handling, payload menu, optional
PLK Manager autoload, native installer branding, and payload packaging.

## Credits

Thanks to all upstream developers and contributors. See the linked repositories
for their individual licenses, attribution requirements, and original source.

## Disclaimer

This project is provided as-is for research and development. Use it only on
hardware and software you own or are authorized to test. The authors are not
responsible for damage, data loss, or other consequences from its use.

## License

This repository remains under the license included with the project sources.

<p align="center">
  <img src="./assets/icon.png" width="128" alt="PS5 Relapse icon" />
</p>

<h1 align="center">PS5 Relapse Autoloader</h1>

<p align="center">
  Native offline AutoLoader with automatic payload loading, by Manohar Padul.<br />
  Supports Relapse firmware <b>7.00–13.60</b>.
</p>

Relapse AutoLoader v0.3.2 installs a cached Wobkot-enabled application on the PS5. The
native ELF is the initial installation tool and does **not** jailbreak a clean PS5
by itself; installing it requires an existing jailbreak and `elfldr`. After
installation, the homescreen app launches Wobkot to jailbreak supported firmware.

## v0.3.2 Wobkot speed update

The browser page and native homescreen app now use Wobkot's PS5 WebKit chain by
default on supported firmware. The existing Relapse chain remains available at
`?chain=relapse` in the browser and `?force=relapse` in the native app. The new
route removes the old five-second pre-exploit wait. Console timings have not yet
been measured, so the release reports the known five-second startup reduction.

Wobkot is included under its MIT license in [`wobkot/`](wobkot/). Its payload
handoff uses this repository's kernel shellcode, ELF loader, firmware symbol
tables, and payload menu. The offline cache is version 34.

## v0.3.1 stability update

v0.3.1 adds safeguards for identified failure paths and improves installer, cache, and payload-menu handling.

- Safe WebKit retries continue without a numerical cap; unsafe states stop immediately.
- Kernel-stage failures no longer report false success.
- AIO cleanup is checked before privilege escalation.
- Added kernel read/write checks and cleanup safeguards.
- ELF-loader readiness checks are bounded; socket-creation failures stop the run.
- An existing ELF loader skips the kernel exploit after initial WebKit/worker setup.
- Payload-send failures restore menu controls; overlapping sends are prevented.
- Installation waits for cache completion and stops on cache errors.
- Separate app identity allows coexistence with itsPLK AutoLoader.
- Game Compressor uses PNG artwork matching the other payload cards.
- Removed the fixed five-second pre-exploit startup wait. The optional PLK Manager
  autoload still waits five seconds after `elfldr` is ready.

**Build and automated checks passed, but crash-free operation is not guaranteed.** These safeguards address identified risks; kernel exploitation and third-party payloads can still freeze the console. Restart the PS5 after an unsafe-state or kernel-stage failure.

The browser-hosted page and the native ELF installer use separate entry points
and both package the Wobkot route.

## Browser-hosted frontend

The default browser route stages its complete bundle locally first. The page
verifies the scripts, firmware offsets, exploit files, and payload ELFs before
starting Wobkot. Once the cache is complete, the same page can be opened again
without downloading the bundle from the internet.

After elfldr is ready, Wobkot keeps the exploit document alive and displays the
payload menu in place. Each payload is sent through the console-side loader on
`127.0.0.1:9021`, so the public static page does not need a server-side socket.

## Requirements

- PS5 firmware supported by the Wobkot route: **7.00–13.60**.
- A PS5 that is already jailbroken for the native installer step.
- `elfldr` listening on console port `9021`.
- Internet access for first-time browser caching; local network access for the native installer transfer and network payload services.

## Current browser setup

1. Open the published page while the PS5 has internet access:
   [manoharpadul.github.io/relapse](https://manoharpadul.github.io/relapse/).
2. Let the **v34** offline-cache step finish. Do not close the browser during this
   first preparation pass.
3. Run the jailbreak. If elfldr is already running, Relapse opens the payload
   path without repeating the kernel chain.
4. On later runs, open the same bookmarked page. The completed cache is used first.

Clearing PS5 browser data removes the cache and requires one more online visit.

## pldmgr autoload

The boot-options card contains a persistent `Autoload pldmgr v0.5.2` toggle.
When enabled, the Wobkot route sends the official 13.60-compatible
`payloads/pldmgr_v0.5.2.elf` as soon as `elfldr` is ready, then opens
`http://<console-ip>:8084/`. When disabled, the in-page payload menu opens instead.

## Network use

The first installation and cache preparation need internet access. After the page
reports that the offline cache is ready, internet access can be disabled, but keep
the PS5 connected to the same local Wi-Fi/LAN as the device used to access its
services.

### Local IP address requirements

The default Wobkot route does not use the PS5 route table for KASLR. A local
IPv4 address is required when using the legacy Relapse route with
`?chain=relapse`, especially on firmware 13.60. Check **Settings > Network > View
Connection Status** and confirm **Obtain IP Address** succeeded. Examples are
`192.168.1.x` on a home router or commonly `172.20.10.x` on an iPhone hotspot.

The internet connection itself is not required. A router with its WAN/internet
disconnected is fine as long as DHCP still gives the PS5 a local IP address. An
iPhone hotspot with cellular data disabled may fail to provide a usable local
interface, depending on the carrier and iPhone state. `127.0.0.1` is only PS5
loopback and does not count as the required Wi-Fi/LAN address.

| Connection | Needed for |
|---|---|
| Internet/WAN | First cache setup and online downloads |
| Wi-Fi or Ethernet/LAN with a local IP address | Native installer transfer, network payload services, and the Relapse fallback |
| Internet after caching | Not required |

Internet after caching is not required for the Wobkot route. The Relapse fallback
uses the PS5 route table for its 13.60 KASLR step, so loopback alone is not
sufficient there. If PS5 browser data is cleared, prepare the cache again while
online.

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

## Wobkot firmware support and legacy Relapse offsets

Wobkot supports PS5 firmware **7.00–13.60**. The following firmware versions
have static symbol tables for the legacy Relapse fallback:

Supported firmware offsets currently include:

`7.00`, `7.01`, `7.20`, `7.40`, `7.60`, `7.61`, `8.00`, `8.20`, `8.40`, `8.60`,
`9.00`, `9.20`, `9.40`, `9.60`, `10.00`, `10.01`, `10.20`, `10.40`, `11.00`,
`11.20`, `11.60`, `12.00`, `12.02`, `12.20`, `12.40`, `12.60`, `12.70`, `13.00`,
`13.20`, `13.40`, `13.42`, and `13.60`.

On 10.60 and 11.40, Wobkot resolves the required symbols from loaded modules at
runtime; these versions do not have static tables for the legacy Relapse fallback.

## Native offline installer

The v0.3.2 native build is documented in [`native/`](native/). It uses the
**itsPLK/ps5-webkit-autoloader v0.5.2** installer and automatic payload interface,
branded **PS5 Relapse AutoLoader — by Manohar Padul**, with the supplied circular
portrait. It defaults to Wobkot on supported 7.00–13.60 firmware. After a successful
jailbreak, **Autoload Payload Manager OFF** shows the payload
menu; **ON** immediately loads the bundled Payload Manager. The choice persists
across launches.

The payload menu is rendered in the outer UI document while the Wobkot exploit
iframe stays alive to send payloads. The existing Relapse chain can be selected
with `?force=relapse`. Other upstream exploit routes keep their unified autoload
behavior. Configure subsequent autoloads through Payload Manager.

The v0.3.2 installer is named:

```text
ps5-relapse-autoloader-installer.0.3.2.elf
```

Installation flow:

1. Jailbreak the PS5 and start `elfldr` on `127.0.0.1:9021`.
2. Send the installer ELF through the existing payload menu.
3. Let the temporary local installer server stage the cache and create the
   homescreen application.
4. Reboot once, then launch **PS5 Relapse AutoLoader** from the PS5 Media section.

The complete release text is in
[`RELEASE_NOTES_v0.3.2.md`](RELEASE_NOTES_v0.3.2.md). The native ELF still needs
testing on a target PS5; a successful compiler build does not confirm behavior on
every firmware or console.

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
- `sw.js` downloads the offline bundle sequentially and writes the v34 marker only
  after the full bundle succeeds.
- `.github/workflows/native-installer.yml` builds the native installer with the
  official PS5 SDK container definition.

## Upstream projects and payload sources

This project is a Relapse-based integration and uses or references the following
open-source projects. Each upstream project retains its own license and credits.

| Project | Role in this project |
|---|---|
| [soniciso1/relapse](https://github.com/soniciso1/relapse) | Original Relapse PS5 WebKit/kernel exploit frontend and firmware-chain lineage |
| [ufm42/wobkot](https://github.com/ufm42/wobkot) | MIT-licensed WebKit and Relapse kernel chain used as the default route |
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

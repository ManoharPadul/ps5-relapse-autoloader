# Native automatic payload installer

The v0.3.1 build uses **itsPLK/ps5-webkit-autoloader v0.5.2** and its installer,
firmware routing, progress UI and cache verification. On the Relapse chain,
Autoload Payload Manager OFF opens the Relapse payload page after success;
ON immediately sends the bundled Payload Manager. The choice is saved on the
console. There is no added delay before jailbreak or before payload autoload.

Branding is **PS5 Relapse AutoLoader — by Manohar Padul**, with the supplied
circular portrait, black page background, installer logo, and favicons.
Upstream authors retain credit for their code and payloads.

After installation, reboot once and launch the homescreen app. The Relapse
payload menu runs in the outer UI document; the exploit iframe is kept alive
to service payload sends. The menu is available only after the chain reports
ELF loader readiness. Payload Manager's own settings can configure subsequent
autoloads. Other upstream exploit routes retain the upstream unified loader.

On 13.60, Wi-Fi/Ethernet must have a usable local IP address. WAN internet is
not needed for the fully cached chain; online downloads still need internet.
Send the installer from a PC using the PS5's LAN IP, not `127.0.0.1`.

Each development build gets a timestamped cache/content version. Reinstall
the newly built ELF and let caching finish to replace the old interface.

This directory describes the separate native-ELF phase for `ps5-relapse-autoloader`.

The upstream `itsPLK/ps5-webkit-autoloader` project supplies the native installer,
PS5 HTTP server, AppCache staging, homescreen-app installation, and Docker SDK
build. The build keeps the upstream frontend and pinned payload dependencies,
including its 13.60 Relapse integration, and applies this fork's visual branding.

The workflow uses the upstream `Dockerfile.sdk`, which installs the PS5 SDK and
native dependencies inside the GitHub Actions runner. It produces an artifact
named `ps5-relapse-autoloader-installer.0.3.1.elf`; it is not the pldmgr payload. Send
that installer ELF once through the already-running elfldr, let it finish the
one-time cache/install flow, then launch the installed homescreen app.

The homescreen icon is generated from this repository's `assets/icon.png`, derived from
the supplied portrait, and embedded into `assets/icon.svg` during the build.

This is intentionally separate from the browser-hosted cache-first page. The
native installer must be tested on the target 13.60 console before it is treated
as a release. A successful compiler build proves the ELF is linked; it does not
by itself prove the PS5 homescreen installation path works on every console.

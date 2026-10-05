# PS5 Relapse AutoLoader v0.3.1

By Manohar Padul.

- Internal app metadata, displayed version and installer filename updated to 0.3.1.
- Installer no longer redirects to the jailbreak app on local-server probe
  failure or while the asynchronous probe is pending. Cache readiness and
  server readiness are required before app installation. Failures stay on the
  installer page; launch the homescreen app separately to start jailbreaking.
- Fresh versioned native cache path: `/app/0.3.1-cache-<build>/`.
- Includes the user-supplied Game Compressor ELF from 2026-10-05.
- After a successful jailbreak, opens the Relapse payload page or sends PLK
  Manager according to the saved autoload toggle.
- If the local ELF loader is already running, opens the same payload controls
  without rerunning the kernel chain.
- Retains upstream retry behavior; no custom stability/retry patches restored.

## Update

Send `ps5-relapse-autoloader-installer.0.3.1.elf` to the ELF loader on your
already-jailbroken PS5. Wait for installation and caching to finish. Reopen the
app and confirm that it displays 0.3.1. Reboot before testing a fresh jailbreak.

Keep Wi-Fi/LAN connected with a usable local IP. Cached content can work without
WAN internet; online services and downloads still need internet access.

Build and automated tests do not establish on-console stability or Game
Compressor firmware compatibility. Existing upstream credits and licenses apply.

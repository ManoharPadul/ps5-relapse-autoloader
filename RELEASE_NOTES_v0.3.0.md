# PS5 Relapse AutoLoader v0.3.0

By **Manohar Padul**. Based on itsPLK's WebKit AutoLoader v0.5.2, with its
installer and jailbreak progress interface, the Relapse portrait/icon, and
the Relapse payload page after a successful Relapse jailbreak.

- No added five-second startup delay or autoload delay.
- Autoload Payload Manager OFF: choose a payload manually.
- Autoload Payload Manager ON: immediately send bundled pldmgr after loader
  readiness; the payload menu remains available.
- Saved ON/OFF preference, one send at a time, and visible send errors.
- New v0.3.0 versioned native cache bundle.
- Visible version is `0.3.0`, without a development suffix. The cache manifest
  and internal `/app/0.3.0-cache-<build>/` path change per build to avoid reusing
  earlier 0.3.0 content. Reinstall this ELF to update it.
- Game Compressor replaced with the file supplied on 2026-10-05 (1,306,064
  bytes; SHA256 `5fec05b8a3cb89bafbc97970d5d68d9f31e6fcde873b5523243890e50836592b`).
  Firmware compatibility and copy/move/compress operations require console testing.
- If the ELF loader is already running, open the payload controls instead of
  reporting "Already jailbroken" as an error. The saved toggle chooses the
  manual menu or immediate PLK Manager autoload without rerunning the kernel chain.
- The exploit iframe remains alive; payload cards render in the outer UI.
- Startup revision: payload card construction, card image requests and menu
  stylesheet loading begin only after ELF loader readiness. The menu reports
  elapsed jailbreak time for on-console comparisons. This removes extra startup
  work; faster exploit completion has not been benchmarked on the PS5.

## Install

1. Jailbreak normally and run an ELF loader.
2. Send `ps5-relapse-autoloader-installer.0.3.0.elf` to the PS5's loader.
   From a PC use the PS5's local IP and the loader's port, usually 9021.
3. Wait for the installer to complete caching and update the homescreen app.
4. Reboot once and launch PS5 Relapse AutoLoader.

On firmware 13.60, keep Wi-Fi or Ethernet connected with a usable local IP.
WAN internet is unnecessary for successfully cached files, but remote downloads
still require internet. Payload Manager's web service normally uses port 8084.
A successful ELF send only confirms transfer, not service startup.

The installer builds with the PS5 SDK. Console installation, jailbreak
stability, rendering, and payload compatibility still require on-device testing.
At the user's request, the recent custom retry limits, terminal-error patches,
and batched logging changes have been removed. Upstream retry, logging and
failure behavior are restored. This also restores upstream's known misleading
success message on some early kernel failures; it is not evidence of readiness.
The post-success payload menu and optional PLK Manager autoload remain.
This rollback is not a verified fix for console freezes.

## Credits

- [itsPLK/ps5-webkit-autoloader](https://github.com/itsPLK/ps5-webkit-autoloader)
- Relapse and the exploit authors credited by upstream
- [itsPLK/ps5-payload-manager](https://github.com/itsPLK/ps5-payload-manager)
- The individual payload authors listed in the repository README

Existing licenses and upstream source credits remain applicable.

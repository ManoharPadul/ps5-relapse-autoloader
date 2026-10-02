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
This revision fixes false-success reporting when the kernel chain stops early,
propagates terminal errors to the outer UI, and stops log polling on terminal
Relapse failures. Embedded log updates use the existing batched poll instead of
forcing hidden-document layout and posting a message for every line.

WebKit retries stop after five safe attempts, or immediately when state cannot
be safely released. Restart the console after a terminal failure; the app does
not automatically reload an uncertain exploit document. The exploit iframe
remains alive. Kernel race logic and firmware offsets are unchanged. These
safeguards do not establish that console freezes or the underlying kernel
failure are fixed; PS5 testing is still required.

## Credits

- [itsPLK/ps5-webkit-autoloader](https://github.com/itsPLK/ps5-webkit-autoloader)
- Relapse and the exploit authors credited by upstream
- [itsPLK/ps5-payload-manager](https://github.com/itsPLK/ps5-payload-manager)
- The individual payload authors listed in the repository README

Existing licenses and upstream source credits remain applicable.

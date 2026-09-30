# PS5 Relapse AutoLoader v0.2.0

## What changed

- Changed the native installer/cache version from `0.1.0` to `0.2.0`.
- Every native build now creates a new versioned AppCache directory and
  completeness marker, so the pointer page can reject an older cached bundle.
- Matched the ELF payload card layout to the working Relapse website's
  PS5-compatible block/float rendering.
- Prebuilt and painted the payload screen before the jailbreak, then reveals the
  same DOM afterward instead of constructing cards during the post-exploit
  compositor transition.
- Removed the native CSS Grid override and eager image flags that could leave
  payload cards blank until the cursor moved over them.
- Kept the exploit document and console-side ELF sender alive behind the payload
  screen, including the 13.60 payload list and optional PLK Manager autoload.
- Removed the unsafe loopback fallback from the native 13.60 KASLR route step and
  added a short wait for Wi-Fi/LAN DHCP initialization.

## Build artifact

```text
ps5-relapse-autoloader-installer.0.2.0.elf
ps5-relapse-autoloader-installer.0.2.0.elf.sha256
```

## Important

This is a native installer/cache ELF, not a standalone jailbreak for a clean
console. Start the supported jailbreak chain and `elfldr` on port `9021`, then
send the installer ELF. Reinstalling this version stages the new cache bundle;
the target PS5 still needs Wi-Fi or Ethernet/LAN for the local console services.

Internet access is not needed after caching, but Wi-Fi or Ethernet/LAN must still
provide a real local IPv4 address. Loopback-only networking cannot satisfy the
13.60 route-based KASLR step. The build must be tested on the target PS5 before
treating the release as fully verified.

Before starting, check **Settings > Network > View Connection Status**. The PS5
must show a successful IP address such as `192.168.1.x` or an iPhone-hotspot
address such as `172.20.10.x`. If it only has `127.0.0.1`, no address, or
`0.0.0.0`, the jailbreak will stop with a local-interface error. This is a LAN
requirement, not an internet requirement.

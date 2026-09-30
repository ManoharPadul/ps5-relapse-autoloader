# PS5 Relapse AutoLoader — Offline Use

PS5 Relapse AutoLoader can run without Internet access after its complete cache
has been installed. Offline does **not** mean that networking can be disabled:
the PS5 still needs Wi-Fi or Ethernet/LAN with a valid local IPv4 address.

## Network requirements

| Connection | Required? | Purpose |
|---|---:|---|
| Internet/WAN | Only for first cache setup | Downloads the complete cached bundle |
| Wi-Fi or Ethernet/LAN | Yes | Required by the PS5 route-based jailbreak step |
| Local IPv4 address | Yes | Must be assigned to the PS5 by DHCP or a configured LAN |
| Internet after caching | No | The cached files run locally |

The PS5 must show **Obtain IP Address: Successful** under:

**Settings → Network → View Connection Status**

Valid examples include:

```text
192.168.1.x       home router or local access point
172.20.10.x       common iPhone Personal Hotspot range
10.x.x.x          private LAN range
```

`127.0.0.1` is only the PS5 loopback address. It is not a Wi-Fi/LAN address
and cannot satisfy the 13.60 route-based KASLR step.

## iPhone hotspot without Internet

An iPhone hotspot can work without WAN Internet **only if it still gives the PS5
a local IP address**. Enable **Personal Hotspot → Allow Others to Join** and,
if necessary, enable **Maximize Compatibility**. Keep the hotspot active while
the PS5 connects.

If the PS5 receives no IP address when cellular data is disabled, the iPhone is
not providing a usable local interface. Use a DHCP-enabled router or access
point with its WAN cable disconnected instead. Internet is not needed, but DHCP
and local Wi-Fi/LAN are needed.

## Offline procedure

1. While online, install the AutoLoader and wait until the complete cache is
   reported as ready.
2. Connect the PS5 to Wi-Fi or Ethernet/LAN.
3. Confirm that the PS5 has a real local IP address.
4. Disable WAN/Internet access if desired, but keep the local network connected.
5. Open the cached Relapse page and start the jailbreak.

If the log says:

```text
kaslr: no local IPv4 interface
```

the PS5 has no usable local IP. Reconnect it to a DHCP-enabled Wi-Fi/LAN and
retry. This error is not caused by the cached files needing Internet access.

## Important

- The native installer itself requires an already-jailbroken PS5 and `elfldr`
  on port `9021`.
- The installer does not jailbreak a clean PS5 by itself.
- Clearing PS5 browser/application data removes the cache and requires another
  online cache-preparation pass.
- Services opened from another device must use the PS5's local IP, for example
  `http://192.168.1.103:8084/` for PLK Manager.


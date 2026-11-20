# PS5 Relapse AutoLoader v0.3.2
By **Manohar Padul**

### Changes
- Added Wobkot's MIT-licensed PS5 WebKit chain as the default route for firmware 7.00–13.60.
- Adapted Wobkot's payload handoff to the bundled kernel shellcode, ELF loader, firmware symbol tables, and payload menu.
- Kept the previous Relapse route available with `?chain=relapse` in the browser and `?force=relapse` in the native app.
- Removed the fixed five-second wait before browser exploitation and updated the offline cache to v34.
- Built the native installer as `ps5-relapse-autoloader-installer.0.3.2.elf`.

The known startup reduction is five seconds. PS5 runtime benchmarks and device validation have not been completed, so exploit duration and reliability may vary by firmware and console.

The Y2JB repositories cover YouTube-based userland execution and setup after kernel access. They do not replace the initial WebKit jailbreak chain used by this project.

Based on [Wobkot](https://github.com/ufm42/wobkot), [itsPLK AutoLoader](https://github.com/itsPLK/ps5-webkit-autoloader), and [Relapse](https://github.com/soniciso1/relapse). See the README for requirements, instructions, and credits.

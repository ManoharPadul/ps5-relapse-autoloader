# PS5 Relapse AutoLoader v0.3.1
By **Manohar Padul**

### Changes
- Improved installer, cache validation, and error handling.
- Added safeguards for identified kernel cleanup and freeze risks.
- Opens payload controls when the ELF loader is already running.
- Fixed Game Compressor card artwork.
- Separate app identity to coexist with itsPLK AutoLoader.
- Refreshed offline cache.

### Update
Send the installer ELF to an already-jailbroken PS5, wait for caching and installation to finish, then open the installed app.

**Testing:** Build and automated checks passed. Console freezes remain possible; crash-free operation is not guaranteed.

Based on [itsPLK AutoLoader](https://github.com/itsPLK/ps5-webkit-autoloader) and [Relapse](https://github.com/soniciso1/relapse). See the README for requirements, instructions, and full credits.

# Native 13.60 installer build

This directory describes the separate native-ELF phase for `ps5-relapse-autoloader`.

The upstream `itsPLK/ps5-webkit-autoloader` project supplies the native installer,
PS5 HTTP server, AppCache staging, homescreen-app installation, and Docker SDK
build. Its bundled exploit frontend is only for the firmware ranges documented by
that project, so this repository does not reuse that frontend. The build workflow
keeps the upstream installer sources and overlays this repository's 13.60 Relapse
frontend and payload bundle before compiling.

The workflow uses the upstream `Dockerfile.sdk`, which installs the PS5 SDK and
native dependencies inside the GitHub Actions runner. It produces an artifact
named `ps5-relapse-autoloader-installer.0.1.elf`; it is not the pldmgr payload. Send
that installer ELF once through the already-running elfldr, let it finish the
one-time cache/install flow, then launch the installed homescreen app.

The homescreen icon is generated from `assets/relapse-icon.png`, derived from
the supplied portrait, and embedded into `assets/icon.svg` during the build.

This is intentionally separate from the browser-hosted cache-first page. The
native installer must be tested on the target 13.60 console before it is treated
as a release. A successful compiler build proves the ELF is linked; it does not
by itself prove the PS5 homescreen installation path works on every console.

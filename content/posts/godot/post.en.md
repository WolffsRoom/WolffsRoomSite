---
tag: Engine · C++
status: Native GXM 2D · experimental 3D
resumo: Godot Engine 4.x ported to PS Vita, exporting straight from the editor.
ficha:
  Base: Godot 4.8-dev7
  2D: Native GXM
  3D: Experimental
  Trophies: In development
links:
  View on GitHub: https://github.com/WolffsRoom/godot4-psvita
  Releases: https://github.com/WolffsRoom/godot4-psvita/releases
---

A custom Godot 4.8-dev7 runtime with native GXM rendering, plus a Windows editor that exports PS Vita VPKs directly. This is not an official Godot release.

## The three parts
- Runtime — Godot built for ARM as libgodot.so, with a Vita system layer, GXM renderers, audio, input and files
- Loader — eboot.bin that loads and starts libgodot.so, shows the boot animation and handles CapUnlocker, logs and data paths
- Windows editor — PS Vita as a built-in export platform

## Highlights
- Portable Godot4Vita.exe: exports with no addon, Python, WSL or VitaSDK
- Turns compatible projects into installable VPKs, with LiveArea and a separate data folder
- LiveArea template picker with preview

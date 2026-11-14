---
titulo: Godot 4 Vita — Release v0.3
tag: Engine · C++
status: v0.3 released
resumo: New Godot 4 for PS Vita release, now with editors for Windows, Linux and macOS.
ficha:
  Version: v0.3
  Editor: Windows, Linux and macOS
  Base: Godot 4.8-dev7
  Showcase: PS Vita VPK
  Requirements: HENkaku/Ensō and kubridge
links:
  Download Showcase (VPK): https://github.com/WolffsRoom/godot4-psvita/releases/download/v0.3/Godot4Vita-v0.3-Showcase.vpk
  v0.3 release on GitHub: https://github.com/WolffsRoom/godot4-psvita/releases/tag/v0.3
  View the project: https://github.com/WolffsRoom/godot4-psvita
---

Godot 4 Vita v0.3 focuses on memory, file reading and the native GXM renderer, and adds PS Vita export on Linux and macOS too.

## Notice
**Godot 4 Vita is a computer program.** This version's editor is available for **Windows, Linux and macOS**: you build and export the game on your PC and install the generated VPK on the Vita. To try it on the Vita, get the [Showcase v0.3 (VPK)](https://github.com/WolffsRoom/godot4-psvita/releases/download/v0.3/Godot4Vita-v0.3-Showcase.vpk), a demo with PCK streaming, audio and 2D/3D scenes.
The macOS build hasn't been tested on a real Mac yet, and the Linux build was made on Ubuntu 22.04.

## What's new
- Portable editors for Windows x64, Linux x86_64 and universal macOS (Intel and Apple Silicon), with the PS Vita platform built in
- game.pck read-ahead on the fourth CPU core (with CapUnlocker), on by default
- Lower memory use: textures go to the GPU on load and the 3D mesh moved to CDRAM (about 24 MiB freed in 3D scenes)
- godot3 audio mode by default, with its own mixer thread
- Separate data folder with game.pck and logs in ux0:data/<folder>/logs/
- GXM 3D fixes (Sprite3D, AnimatedSprite3D, Label3D) and a lighter 2D canvas
- On-console shader compiler, experimental and off by default
- SelfTest VPK that runs every device test in about 6 minutes

## Installation
- Download the editor for your OS from the [release page](https://github.com/WolffsRoom/godot4-psvita/releases/tag/v0.3), extract the whole folder and keep vita/ next to the executable
- In Project > Export, add the PS Vita preset and export the .vpk
- Install the VPK with VitaShell and copy the generated data folder to ux0:data/
- v0.2 projects must be re-exported with the v0.3 editor

## Known limitations
- GXM 3D is still experimental
- CanvasItem shaders and materials aren't rendered yet
- Trophies are packaged but don't unlock yet

---
tag: Port · GameMaker · PS Vita
status: 81% · Playable
resumo: Deltarune, chapters 1 to 5, on PS Vita.
titulo_barras: Review by chapter
barras:
  Chapter 1: 100
  Chapter 2: 100
  Chapter 3: 95
  Chapter 4: 85
  Chapter 5: 80
ficha:
  Status: Playable
  Source: Steam v0.0.253
  Runtime: Butterscotch + VitaGL + OpenAL
  Build: Deltarune-v0.81.vpk
  Trophies: Yes (NoTrpDrm)
video_legenda: DeltaruneVita trailer
links:
  Download VPK (v0.81): https://github.com/WolffsRoom/DeltaruneVita/releases/download/v0.81/Deltarune-v0.81.vpk
fontes:
  View on GitHub (PS Vita): https://wolffsroom.github.io/WolffsStore/WolffsRoom/DeltaruneVita/
  Releases (PS Vita): https://wolffsroom.github.io/WolffsStore/WolffsRoom/DeltaruneVita/releases/
---

Unofficial port of DELTARUNE, chapters 1 to 5. It runs the official GameMaker data (Windows/Steam) on a Vita-focused Butterscotch implementation, with VitaGL for graphics and OpenAL for audio. The repository and releases do not include the commercial game data.

## Chapter status
- Chapter 1 — everything works
- Chapter 2 — small performance drops in some rooms
- Chapter 3 — some minigames stutter on first load
- Chapter 4 — some rooms still need optimization
- Chapter 5 — optimization incomplete; full completion not verified yet

## Highlights
- Vita controls with optional touch
- Configurable graphics and audio
- Console borders
- Language and mod support
- Trophies
- Native video playback
- Patchers that build the Vita data from your copy of the game

## Requirements
- Hacked PS Vita
- kubridge (kubridge.skprx)
- FdFix (fd_fix.skprx), unless you use rePatch
- libshacccg.suprx installed on the Vita
- Official, unmodified DELTARUNE install from Steam (v0.0.253)
- CapUnlocker, to improve performance
- NoTrpDrm, for trophies (optional)

## Installation
- Build the Vita data with one of the patchers
- Copy the generated deltarune folder to ux0:data/
- Install the VPK on the Vita

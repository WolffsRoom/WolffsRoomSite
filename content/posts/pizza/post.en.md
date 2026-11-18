---
tag: Port · GameMaker · PS Vita
status: v0.62 · Playable
resumo: "v0.62 update of the SAGE 2019 Demo (v14) port, improving GPU residency, palette shading, input and pause controls."
chamada: Pizza Tower SAGE 2019 is now on PS Vita! Three playable v14 demo stages at 60 FPS.
ficha:
  Status: Released · Playable (95% progress)
  Version: v0.62
  Original demo: Pizza Tower SAGE 2019 (v14)
  Original game: Tour de Pizza
  Original engine: GameMaker
  Runtime: Butterscotch + VitaGL + OpenAL
  Title ID: PTSAGE001
  Data: ux0:data/pizzatowersage/data.win
video_legenda: PS Vita port trailer
links:
  Download VPK: https://github.com/WolffsRoom/PizzaTowerSage2019Vita/releases/download/v0.62/PizzaTowerSAGE-v0.62.vpk
  Download data: https://drive.google.com/file/d/1CBof60EExpF4IrZMhyix6CvRicqSONRA/view?usp=sharing
fontes:
  GitHub: https://github.com/WolffsRoom/PizzaTowerSage2019Vita
  Official demo: https://pizzatowerguy.itch.io/pizza-tower-demo
  Pizza Tower Wiki: https://pizzatower.wiki/SAGE_2019_Demo
clock:
  CPU / GPU: 500 MHz / 222 MHz
  Performance: 60 FPS (as reported by project testing)
---

Unofficial PlayStation Vita port of the free **Pizza Tower SAGE 2019 Demo (v14)**, newly released as **v0.62**. Powered by Butterscotch, VitaGL, and OpenAL. The demo is playable from start to finish, with **95% overall project progress**.

## What's new in v0.62

- Permanent BC3 (DXT5) residency for all 35 texture pages (~87 MiB), avoiding mid-frame texture evictions and synchronizing GPU work on room transitions
- SAGE Blue Peppino costume via the pal_swapper shader without extra uncompressed VRAM texture atlases
- Dash / Super Jump fix: invalid VK_NOKEY settings can no longer trigger unintended Super Jumps at Mach 3
- Fixed level selector activation and analog drift: Up now uses D-pad Up (or configured touch Up) to avoid phantom inputs
- **Start** opens the original SAGE pause menu; **Select** opens the port's settings overlay


- Three playable stages: **Pizzascape**, **Oregano Desert**, and **The Snick Challenge**
- 60 FPS in hardware tests with VitaGL rendering
- Fixed Super Jump launch on Cross (Jump) or directional release
- Analog stick deadzone calibration fixes accidental ducking
- SGX543-compatible palette shader and restored colors
- Streaming OpenAL audio to reduce memory usage and distortion
- Cleaner settings fonts, PlayStation glyphs, custom LiveArea and manual

## Installation

- Download the [v0.62 VPK](https://github.com/WolffsRoom/PizzaTowerSage2019Vita/releases/download/v0.62/PizzaTowerSAGE-v0.62.vpk) and install via VitaShell
- Get the original free demo from the [official Pizza Tower itch.io page](https://pizzatowerguy.itch.io/pizza-tower-demo)
- Extract data.win and copy to **ux0:data/pizzatowersage/data.win**
- The Download data button preserves the previously shared external archive; verify it contains v14 demo data
- Launch the game from LiveArea

## Requirements

- Homebrew-enabled PS Vita with HENkaku/Ensō
- kubridge.suprx, FdFix and libshacccg.suprx
- Original SAGE 2019 Demo (v14) data.win, not included with the VPK

## Credits

- **PS Vita port:** Wolff's Room
- **Original game:** Tour de Pizza
- **Runner:** Butterscotch with VitaGL and OpenAL

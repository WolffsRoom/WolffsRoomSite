---
titulo: 'Horizon Chase Turbo: Optimization Patch'
tag: Mod · PS Vita
status: Published · 05/2026
resumo: Tweaks Unity quality and graphics settings to improve performance.
video_legenda: Demo by Titi Clash
ficha:
  Status: Published
  Game version: PCSH10315
  Posted: 15/05/2026
  Archive password: wolffsroom
links:
  Google Drive: https://drive.google.com/file/d/1yzabN4ZbU9WIyPoEBrCsT_dpn0gtq2dd/view?usp=sharing
  MediaFire: https://www.mediafire.com/file/3fsdmthpxlwqb4h/Patch+PCSH10315.rar/file
  Original post: https://wolffsroom.wordpress.com/2026/05/15/horizon-chase-turbo-patch-de-otimizacao/
---

Optimization patch for Horizon Chase Turbo on PS Vita. It changes Unity settings to ease the load on the GPU and video memory. It comes in three options: 736×416, 832×480 and 832×480 at 30 FPS.

## What changes
- 832×480 resolution (the Vita default is 960×544)
- 16-bit video buffer to reduce VRAM use
- VSync on
- Low graphics profile from the start
- Anisotropic filtering off
- Accelerometer frequency set to zero

## Reported performance
- With overclock: from about 35 to 45 FPS
- Without overclock: a locked 30 FPS, versus 20 to 29 in the original

## Requirements
- Hacked PS Vita (HENkaku/Enso)
- Game installed (PCSH10315)
- rePatch plugin installed and enabled

## Installation
- Download and extract the archive
- Connect the Vita over USB or FTP
- Copy one of the three folders to ux0:rePatch/
- Restart the Vita and open the game

## Credits
- Titi Clash — demo video
- Tools: VitaShell and UABEA

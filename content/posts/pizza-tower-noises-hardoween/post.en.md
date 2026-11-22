---
titulo: "Pizza Tower - Noise's Hardoween Demo"
tag: Port · GameMaker · PS Vita
status: v0.41 · Playable
resumo: "Noise's Hardoween Demo reaches PS Vita in v0.41 with graphics fixes and automatic first-boot data.win optimization."
chamada: "The Noise arrives on PlayStation Vita! The Halloween-themed Pizza Tower demo with native rendering, texture optimizations and improved audio."
ficha:
  Status: Released · Playable (95% progress)
  Version: v0.41
  Original demo: "Pizza Tower: Noise's Hardoween Demo"
  Original creators: Tour de Pizza
  Original engine: GameMaker
  Runtime: Butterscotch + VitaGL + OpenAL
  Title ID: PTNHW0001
  Game data: ux0:data/noisehardoween/data.win
links:
  Download VPK: https://github.com/WolffsRoom/PizzaTowerNoisesHardoween/releases/download/v0.41/PizzaTowerHardoween-v0.41.vpk
  Download data: https://drive.google.com/file/d/1X9lZ5Y_hcBPbsNbI_hIj6bz8I8johboy/view?usp=sharing
fontes:
  GitHub: https://github.com/WolffsRoom/PizzaTowerNoisesHardoween
  Original demo: https://pizza-t0w3rfan.itch.io/noises-hardoween
clock:
  Performance: 60 FPS (as reported by project tests)
---

Unofficial PlayStation Vita port of the free **Pizza Tower: Noise's Hardoween Demo**, released as **v0.41**. Play as **The Noise** through the Halloween-themed demo. The project is marked **95% complete**.

## What's new in v0.41

- **Knight transformation GPU crash fix:** SGX543-compatible palette shaders support The Noise's unlockable Halloween costumes and enemy color palettes.
- **Native-resolution textures:** active texture pages at 2048×2048 for sharper backgrounds, sprites and HUD.
- **Background rendering fixes:** higher shader precision prevents red seam lines and texture artifacts.
- **Layer ordering fixes:** The Noise no longer renders behind doors and ladders.
- **Optimized audio:** on-demand OpenAL streaming reduces memory usage.
- **Automatic optimization:** the port prepares the game's texture atlases on the Vita during the first launch.

## Installation

- Download the **v0.41 VPK** and install it using VitaShell.
- Obtain the original **data.win** from the free demo using **Download data**, or from the [original demo page](https://pizza-t0w3rfan.itch.io/noises-hardoween).
- Copy **data.win** into **/ux0:/data/noisehardoween/** (VitaShell notation: **ux0:data/noisehardoween/data.win**).
- Launch the game from LiveArea.

## Important notes

- **The first launch may take longer.** The VPK automatically optimizes the game's **data.win** texture atlases for PS Vita. No external patcher or second device is necessary.
- A backup of the original data is saved as **data.original.win** during first-boot optimization.
- The VPK does not contain the demo's proprietary data. You must provide a compatible original **data.win**.

## Requirements

- Homebrew-enabled PS Vita (HENkaku/Ensō).
- **kubridge**, **FdFix** and **libshacccg.suprx**.
- Original demo **data.win**.

## Credits

- **PS Vita port:** Wolff's Room
- **Original demo:** Tour de Pizza
- **Demo availability:** Pizza Tower Fan (itch.io)
- **Runtime:** Butterscotch, VitaGL and OpenAL

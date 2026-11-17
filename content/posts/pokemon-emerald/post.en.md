---
novidade: Update
titulo: Pokémon Emerald Voxel 3DS — PT-BR v0.5.1
tag: Native port · PS Vita · PT-BR · v0.5.1
status: Available · v0.5.1
resumo: Native PS Vita Pokémon Emerald v0.5.1, improved wild Pokémon, Brazilian Portuguese and new camera controls.
chamada: Pokémon Emerald v0.5.1 for PS Vita — overworld encounters, voxel 3D and PT-BR localization.
ficha:
  Version: v0.5.1
  Wolff's Room edition: PT-BR · LiveArea · Manual · Camera
  Original port: HctrRB
  Platform: PS Vita / PSTV
  Technology: Native ARM code · vitaGL
links:
  Download VPK (Google Drive): https://drive.google.com/file/d/1ZNVd7j6EZyGgYTHuwIL-Edj6r57hJCGn/view?usp=sharing
fontes:
  Original port source (HctrRB): https://github.com/HctrRB/pokeemerald-vita-3ds
  PT-BR pull request: https://github.com/HctrRB/pokeemerald-vita-3ds/pull/3
  Original translation (Pokebat): https://pokebat.net/2017/04/pokemon-emerald-portugues-pt-brgba.html
---
**Pokémon Emerald** has an unofficial native PS Vita port developed by **HctrRB**, based on the [pret/pokeemerald](https://github.com/pret/pokeemerald) decompilation. It is not an emulator: the game's C code is compiled for Vita ARM, while a platform layer replaces GBA hardware functions.

Using **vitaGL** and features from [Emerald 3DS](https://github.com/ZallaxDev/emerald-3ds), the port offers a modern 3D presentation of the original adventure.

## What's new in v0.5.1 — Visible Wild Pokémon
- **Procedural overworld pool:** up to 48 wild Pokémon (`VW_POOL_MAX = 48`) independent of the 12 active sprite slots, allowing encounters throughout the map like NPCs.
- **Neighbor map pre-population:** valid encounter tiles sampled in advance, scanning up to 24 tiles of connected map layouts with species prefetching.
- **25° camera-aware streaming:** asymmetric north/south ranges (`VW_VIEW_NORTH = 20`, `VW_SHOW_NORTH = 24`, `VW_HIDE_NORTH = 26`), entry/exit hysteresis and two-sprites-per-frame limit.
- **Spawn and animation fixes:** no repeat pop-ins on map changes; growth and grass/water rustling are reserved for actual spawns, respawns and in-view materializations.

## Original port features
- Live voxel 3D overworld built from maps, with sun, shadows, day/night, and weather
- 3D battle stages drawn from the map where battles start
- Touch menus with five themes, replacing the GBA's menus and dialog boxes
- HGSS-style follower Pokémon, accelerated clock, time-based encounters, and optional QoL features

## Wolff's Room improvements
- Reviewed the **Brazilian Portuguese localization**, including new voxel UI labels and gameplay text.
- Adapted overflowing text with marquee animations and translated town descriptions for the different UI themes.
- Added **right-stick camera controls**, experimental **first-person view** and optional camera-facing 2D tree sprites.
- Removed the **vitaGL startup splash** from the customized build.
- Updated the title-screen labels (**Versão Esmeralda** and **PRESSIONE START**), LiveArea artwork and Portuguese manual.

*The new camera and first-person controls are experimental. We recommend using the default camera/graphics preset for initial gameplay.*

## Installation
- Download the v0.5.1 VPK using the Google Drive download button
- Install it with VitaShell on a homebrew-enabled PS Vita
- Launch the game from LiveArea
- Back up existing saves before replacing an earlier version

## Credits and references
- **Original port:** [HctrRB](https://github.com/HctrRB/pokeemerald-vita-3ds)
- **PT-BR edition:** Wolff's Room
- **Translation reference:** [Pokebat](https://pokebat.net/2017/04/pokemon-emerald-portugues-pt-brgba.html)
- **Game decompilation:** [pret/pokeemerald](https://github.com/pret/pokeemerald)
- **3D features:** [Emerald 3DS](https://github.com/ZallaxDev/emerald-3ds)
- **Fonts referenced:** [Pokémon Classic](https://www.dafont.com/pt/pokemon-classic.font) and [Pokémon Font Meme](https://fontmeme.com/pt/fonte-de-pokemon/)
- **LiveArea art reference:** [Gen 3 Pokémon 3DS-style icons](https://www.reddit.com/r/pokemon/comments/1n01ybd/i_did_3ds_menu_icons_for_gen_3_pokemon_games/?i=2)

## Notes
- Unofficial port, not affiliated with Nintendo, Game Freak, or The Pokémon Company.
- VitaSDK build completed; the latest title-banner palette fix has not yet been visually confirmed on hardware.

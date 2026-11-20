---
novidade: Update
titulo: Pokémon Emerald Voxel 3DS — PT-BR v0.5.8
tag: Native port · PS Vita · PT-BR · v0.5.8
status: Available · v0.5.8
resumo: Pokémon Emerald v0.5.8 PT-BR on PS Vita with expanded menus, improved stability and screen-aligned free-look controls.
chamada: New v0.5.8 PT-BR edition with upgraded native menus, voxel 3D and intuitive free-look controls.
ficha:
  Version: v0.5.8
  Wolff's Room edition: PT-BR · LiveArea · Manual · Camera
  Original port: HctrRB
  Platform: PS Vita / PSTV
  Technology: Native ARM code · vitaGL
links:
  Download VPK (Google Drive): https://drive.google.com/file/d/1Tt_DDvS6_LOhLS4HcNvHRahz3VvLs1_v/view?usp=sharing
fontes:
  Original port source (HctrRB): https://github.com/HctrRB/pokeemerald-vita-3ds
  PT-BR pull request: https://github.com/HctrRB/pokeemerald-vita-3ds/pull/3
  Original translation (Pokebat): https://pokebat.net/2017/04/pokemon-emerald-portugues-pt-brgba.html
---
**Pokémon Emerald** has an unofficial native PS Vita port developed by **HctrRB**, based on the [pret/pokeemerald](https://github.com/pret/pokeemerald) decompilation. It is not an emulator: the game's C code is compiled for Vita ARM, while a platform layer replaces GBA hardware functions.

Using **vitaGL** and features from [Emerald 3DS](https://github.com/ZallaxDev/emerald-3ds), the port offers a modern 3D presentation of the original adventure.

## What's new in v0.5.8 — Native menus and fixes
- **Expanded native interface:** upgraded Pokéblock Case, post-catch Pokédex page, party choices, Bag, and boxed Pokémon summary.
- **Battle Frontier and Battle Pyramid:** more native menus for party selection, the Pyramid Bag and challenge workflows.
- **Easy Chat and PokéNav:** additional campaign interactions, tutorials, word selection, maps and Frontier Pass pages.
- **GBA mini-games retained:** Contest and other full-screen GBA scenes use the original 816×544 presentation with black side bars.
- **v0.5.8 fixes:** item, menu and dialogue fixes, including a crash fix when reading mail from the Bag.
- **Visible wild Pokémon:** existing procedural overworld encounter improvements remain available.

## Original port features
- Live voxel 3D overworld built from maps, with sun, shadows, day/night, and weather
- 3D battle stages drawn from the map where battles start
- Touch menus with several themes, while retaining the original GBA layout where needed
- HGSS-style follower Pokémon, accelerated clock, time-based encounters, and optional QoL features

## Wolff's Room improvements
- Updated the **Brazilian Portuguese localization**, covering 14,253 game-text entries and over a thousand native UI dictionary strings, including the v0.5.8 additions.
- Adapted overflowing text with marquee animations and translated town descriptions for the different UI themes.
- Updated **right-stick free-look** with **screen-aligned character movement** when rotating the camera; optional **first-person view** and camera-facing foliage.
- Removed the **vitaGL startup splash** from the customized build.
- Updated the title-screen labels (**Versão Esmeralda** and **PRESSIONE START**), LiveArea artwork and Portuguese manual.

*Camera and first-person options remain experimental. Newly integrated menus and this PT-BR build still require a complete physical Vita test; use the default camera if you notice visual issues.*

## Installation
- Download the v0.5.8 VPK using the Google Drive download button
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
- The v0.5.8 VitaSDK build completed, including VPK/LiveArea and vitaGL NoSplash checks. Its expanded UI and camera-relative controls still need a full physical PS Vita test.
- The upstream maintainer is preparing a multilingual pipeline; this local PT-BR build is separate from the pending upstream localization PR.

---
titulo: YouTube on Vita
tag: YouTube on TV · Cobalt · PS Vita
status: v0.65 · Update
resumo: 'YouTube on Vita v0.65: Vertical Shorts, native controller shortcuts, aspect-ratio modes, UI sounds and improved
  playback/downloads.'
chamada: '**The real YouTube on TV experience, brought to PlayStation Vita through Cobalt.**


  **New in v0.65:** Vertical Shorts, new controls, aspect-ratio modes and interface improvements.


  Full and Lite versions available.'

ficha:
  Version: v0.65 · Update
  Platform: PlayStation Vita / Vita3K
  Engine: Cobalt / Starboard 15 / VitaGL
  Video: H.264 / AAC · up to 720p; Full HD experimental
  Controls: Buttons, analog sticks, touch and microphone
  Builds: Full (extended RAM) / Lite (lower RAM usage)
  Title IDs: YTVCB0001 (Full) / YTVCB0002 (Lite)
  Requirement: kubridge v0.3.1 or newer
links:
  YouTube: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/YouTube.vpk
  YouTube Lite: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/YouTube-Lite.vpk
fontes:
  Repository and README: https://github.com/WolffsRoom/YouTubeOnVita
---

Hey everyone! Wolff here.

**YouTube on Vita v0.65** is now available! The original **YouTube on TV** experience on PlayStation Vita now includes new controls, features and performance improvements since the first public release.

## What's new in v0.65

- **Shorts and Vertical Mode:** portrait video playback with gesture navigation while holding the Vita vertically. Inverted screen mode is still experimental.
- **Player:** H.264 playback up to 720p, Aspect Ratio modes (Original, Zoom and Stretch), Bilinear/Nearest filtering and improved support for unusual video sizes.
- **Controls:** left analog-stick navigation, right-stick volume/brightness shortcuts and Player settings on Triangle.
- **Interface:** complete 60 FPS startup animation, adjustable native UI sounds and refined Add-ons.
- **Sleep Timer:** 5-minute option, final 60-second countdown and audio alerts.
- **Downloads:** improved MP3/MP4 handling, audio conversion during downloading, paginated files and notices when a requested quality is unavailable.
- **Stability:** improved memory/GPU handling, network reconnection and preservation of previous-session logs.

## Which version should I download?

Install using **VitaShell**. Full and Lite have separate LiveArea bubbles and can coexist.

- **YouTube Full — recommended:** extended RAM for better video playback.
- **YouTube Lite — lower RAM usage:** better compatibility when keeping other apps in the background.

**Requirement:** install [kubridge v0.3.1 or newer](https://github.com/bythos14/kubridge/releases/latest) under `*KERNEL` and reboot. Older versions may crash shortly after the startup animation. You do not need to erase the app's settings or sign-in data when updating.

## Known limitations

**Full HD, Inverted screen and some Shorts controls remain experimental.** AdBlock is partial, MP4 downloads may use a lower resolution than requested, and occasional crashes when switching videos are still under investigation. The Square-button comments shortcut is not implemented yet.

If you encounter problems, share `cobalt_boot_prev.log`, `starboard15_prev.log` and the `.psp2dmp` dump if available.

For setup and technical details, see the [YouTube on Vita README](https://github.com/WolffsRoom/YouTubeOnVita#readme).

**Vita means life!**

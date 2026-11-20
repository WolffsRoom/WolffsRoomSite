---
titulo: YouTube on Vita
tag: YouTube on TV · Cobalt · PS Vita
status: v0.58 · First Release
resumo: The genuine YouTube on TV experience on PS Vita, with sign-in, touch controls, native Add-ons and video playback up to 720p.
chamada: YouTube on Vita v0.58 is here! The first public release, available in Full and Lite editions.
ficha:
  Version: v0.58 · First Release
  Platform: PlayStation Vita / Vita3K
  Engine: Cobalt / Starboard 15 / VitaGL
  Video: H.264 / AAC · up to 720p
  Controls: Buttons, touchscreen and built-in microphone
  Builds: Full (extended RAM) / Lite (lower RAM usage)
  Title IDs: YTVCB0001 (Full) / YTVCB0002 (Lite)
links:
  YouTube Full - Recommended download: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.58/YouTube.vpk
  YouTube Lite - Lower RAM usage: https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.58/YouTube-Lite.vpk
  GitHub Release v0.58: https://github.com/WolffsRoom/YouTubeOnVita/releases/tag/v0.58
fontes:
  Repository and README: https://github.com/WolffsRoom/YouTubeOnVita
---

Hey everyone! Wolff here.

**YouTube on Vita v0.58** is here as its **first public release**! This port brings the genuine **YouTube on TV** experience to PlayStation Vita using Cobalt and the console's native features.

## Features

- **Real YouTube interface:** browsing, search, account sign-in and TV player controls.
- **Native input:** physical buttons, touchscreen and microphone integration for supported voice features.
- **Video playback:** H.264/AAC up to 720p, with support for up to 60 FPS when the video and device allow it.
- **Add-ons:** screenshots, sleep timer, black/dimmed screen, performance settings and navigation sounds.
- **Downloads:** MP4 video and MP3 audio, with square artwork on newly downloaded songs.
- **Session protection:** HTTPS connections and encrypted local session storage.

## Cobalt and performance

**About interface FPS:** Cobalt does not need to redraw an unchanged screen. An FPS counter may show low values in static menus even when navigation is responsive, helping save processing work and battery life.

Playback has also been tested at **222 MHz CPU / 111 MHz GPU**, with satisfactory results for the tested content.

## Which version should I download?

Install either VPK using **VitaShell**. The two editions have separate LiveArea bubbles. No PC or companion server is needed.

- **YouTube Full — recommended:** YouTube.vpk uses extended RAM for video playback.
- **YouTube Lite — lower memory usage:** YouTube-Lite.vpk uses normal RAM for better compatibility with suspended background apps.

## Known limitations

**AdBlock is partial** and cannot remove every YouTube ad. Some videos are restricted by their encoding or content. Occasional crashes while switching HD videos, especially during downloads, are still being investigated.

For build instructions, Google sign-in details and more screenshots, see the [project README](https://github.com/WolffsRoom/YouTubeOnVita).

**Vita means life!**

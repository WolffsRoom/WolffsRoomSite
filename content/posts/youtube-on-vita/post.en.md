---
titulo: 'Youtube - Unofficial client for PS Vita (alpha)'
tag: Unofficial YouTube client · PS Vita
status: Alpha v0.34 · Real hardware testing
resumo: Genuine YouTube on TV interface on PS Vita, with sign-in, touch controls and H.264/AAC playback up to 720p.
chamada: YouTube on real PS Vita hardware, powered by Starboard 15 with touch input and video up to 720p.
ficha:
  Version: Alpha v0.34 (experimental)
  Platform: Starboard 15 / VitaGL (a direct GXM renderer is planned)
  Controls: Buttons and touchscreen gestures
  Video: H.264 up to 720p, up to 60 fps
  Status: Testing on real hardware
  Title ID: YTVCB0001
  Recommended plugin: CapUnlocker (four CPU cores; optional)
links:
  Wolff's Store (PS Vita): https://wolffsroom.github.io/WolffsRoomSite/
fontes:
  GitHub - YouTubeOnVita: https://github.com/WolffsRoom/YouTubeOnVita
---

An experimental, unofficial YouTube client for the PlayStation Vita, bringing the **genuine YouTube on TV interface (Starboard 15)** to both real hardware and Vita3K. Alpha v0.34 replaces the earlier v0.22 testing-only status.

## What currently works in testing

- The genuine YouTube on TV interface runs on real PS Vita hardware and in Vita3K.
- Smooth navigation: the interface renders at up to 60 fps on hardware.
- D-pad and buttons, plus touchscreen gestures: tap to select, swipe to scroll, two-finger tap to go back.
- Hardware H.264/AAC playback from 240p to 720p, including 60 fps streams.
- Sign-in and settings are saved between sessions.
- Player controls: pause/resume and captions.
- Uses all four CPU cores when the CapUnlocker plugin is installed.

## Alpha status and limitations

**This is experimental software, not a stable release.** Known issues: text shadows over videos and thumbnails show as dark boxes, the lyrics view of music videos does not play, and an occasional crash can still happen (under investigation). 1080p is not available because the Vita's video decoder is limited to 720p for apps. Playback speed controls, VP9/AV1 and protected content are not supported.

## Installation

- Download and install alpha v0.34 **through Wolff's Store on PS Vita only**. The file link is provided in the Store catalog, not as a separate web download button.
- **CapUnlocker is recommended, not required.** When enabled in taiHEN, it allows the app to use all four CPU cores. The Store displays a warning before installation.
- Restart your Vita after enabling the plugin when necessary.
- No companion PC or server is required to access the app's interface.

## Notes

QR sign-in, login persistence and playback audio have been verified in testing on a real PS Vita. This remains an alpha release and occasional crashes are still being investigated.

## Credits

- PS Vita port: Wolff's Room
- Interface: YouTube on TV / Starboard 15 (Cobalt)
- Rendering: VitaGL (direct GXM backend planned)

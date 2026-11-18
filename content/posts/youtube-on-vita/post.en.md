---
titulo: YouTube on Vita — Alpha
tag: App · PS Vita
status: Experimental alpha
resumo: The real YouTube on TV experience on PS Vita, powered by an experimental port of Google's Cobalt and Starboard.
chamada: The actual YouTube on TV interface on PlayStation Vita — not a custom-made lookalike.
ficha:
  Version: Alpha v0.22 (experimental)
  Runtime: Google Cobalt Evergreen 5.50.2
  Platform: Starboard 15 / VitaGL
  Controls: Buttons and touchscreen
  Status: Testing
fontes:
  Source and development: https://github.com/WolffsRoom/YouTubeOnVita
---
**YouTube on Vita** is an unofficial PlayStation Vita client built around the real **YouTube on TV** experience seen on smart TVs and consoles, rather than a hand-built imitation.

It brings the **Google Cobalt Evergreen** runtime and **Starboard** platform layer to the Vita, connecting graphics, memory, networking, controls, audio, and media decoding to native Vita APIs.

## What currently works in testing

- The genuine YouTube on TV interface loads and renders in Vita3K.
- D-pad and button navigation, plus experimental touchscreen support.
- Page loading, thumbnails, side navigation, and service video requests.
- Experimental H.264/AAC playback using Vita native decoders.
- Shader cache, startup, memory, and audio optimizations.
- A test video advanced through playback and reached end of stream in Vita3K.

## Alpha status and limitations

**This is experimental software, not a stable release.** Real-hardware performance, audio under load, stability, and login persistence need further work. QR sign-in and other account features have not been fully verified. Some codecs, resolutions, streams, and protected content are unsupported.

This project is not affiliated with or endorsed by Google, YouTube, or Sony.

## Distribution

Installable alpha builds will be distributed **exclusively through the Wolff's Store app on PS Vita**, when available. **The VPK will not be downloadable from this website or GitHub releases.**

Follow development on the [YouTubeOnVita repository](https://github.com/WolffsRoom/YouTubeOnVita).

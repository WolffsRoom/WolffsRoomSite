<div align="center">

<img alt="Wolff's Room" src="https://github.com/user-attachments/assets/93573c5d-c8de-4888-8ec9-0bf8ef138549" />

<br>

**The official home of Wolff's Room projects.**

*PlayStation Vita ports, homebrew, mods, translations, reviews, and more.*

[**Visit Website**](https://wolffsroom.github.io/WolffsRoomSite/) · [**GitHub**](https://github.com/WolffsRoom) · [**Submit a Post**](https://github.com/WolffsRoom/WolffsRoomSite/issues/new?template=novo-post.yml)

![Platform](https://img.shields.io/badge/Platform-PS%20Vita-FF0033?style=flat-square)
![Hosting](https://img.shields.io/badge/Hosting-GitHub%20Pages-212121?style=flat-square&logo=github)
![Status](https://img.shields.io/badge/Status-Online-brightgreen?style=flat-square)

</div>

---

## Overview

**Wolff's Room** is an independent project hub dedicated to the PlayStation Vita homebrew community.

The website brings together game ports, homebrew applications, translations, mods, reviews, and development updates in one place.

Featuring a custom **pixel-art interface**, interactive animations, UI sounds, community polls, and support for **English and Brazilian Portuguese**.

### What's Inside

- **Ports:**
  - Games adapted to run on PlayStation Vita.
- **Apps and Tools:**
  - Homebrew applications, utilities, and plugins.
- **Translations and Mods:**
  - Community-driven improvements and localization projects.
- **Journal and News**
  - Releases, announcements, and development progress.
- **Community Polls** — Vote on upcoming projects and ideas.

---

## How It Works

The website is automatically generated from Markdown content using Python and deployed through GitHub Actions.

```text
      Markdown Posts + Assets
                |
          Python Builder
         (tools/build.py)
                |
          Static Website
             (_site/)
                |
          GitHub Actions
                |
           GitHub Pages
                |
           Wolff's Room
```

### Project Structure

| Path | Description |
|---|---|
| `content/posts/<slug>/` | Individual project posts, metadata, and screenshots. |
| `assets/` | Website graphics, fonts, textures, and audio. |
| `tools/build.py` | Static website generator. |
| `tools/template.html` | Layout, styles, animations, and interactive elements. |
| `tools/issue_to_post.py` | Converts GitHub Issues into website posts. |
| `poll-backend/` | Cloudflare Worker backend for community polls. |
| `visitors-backend/` | Anonymous visitor statistics. |
| `.github/workflows/pages.yml` | Automatic deployment to GitHub Pages. |
| `.github/workflows/novo-post.yml` | Automated post creation from GitHub Issues. |

---

## Submit a Post

Want to add a new project or update an existing post?

Use the [**New Post Form**](https://github.com/WolffsRoom/WolffsRoomSite/issues/new?template=novo-post.yml).

For detailed instructions, see [COMO-POSTAR.md](COMO-POSTAR.md).

---

## Links

- **Website:** https://wolffsroom.github.io/WolffsRoomSite/
- **GitHub:** https://github.com/WolffsRoom
- **YouTube:** https://www.youtube.com/@WolffsRoom

---

## Disclaimer

_Wolff's Room is an independent, unofficial fan project and is not affiliated with Sony Interactive Entertainment or the original developers and publishers._

All trademarks, games, characters, and original artwork belong to their respective owners.

<div align="center">

---

*Wolff's Room © 2026*

</div>

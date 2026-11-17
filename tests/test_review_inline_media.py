"""Review media stays in editorial order, without an auto screenshots section."""
import sys
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build


class ReviewMediaTests(unittest.TestCase):
    def test_p4g_images_and_gifs_inline(self):
        post = build.load_post("p4g")
        html = build.article(post, "pt")
        assets = ["modelo-personagens.gif", "combate.gif", "inaba.jpg", "teddie.gif"]
        inline_sources = re.findall(r'<figure class="wr-review-media".*?<img src="([^"]+)"', html)
        self.assertEqual(inline_sources, [f"posts/p4g/{filename}" for filename in assets])
        self.assertNotIn("Capturas de tela", html)
        self.assertEqual(html.count('class="wr-review-media"'), 4)

    def test_god_of_war_images_and_gif_inline(self):
        post = build.load_post("god-of-war-ragnarok")
        html = build.article(post, "pt")
        assets = ["captura-3.gif", "capa.jpg", "combate.gif"]
        inline_sources = re.findall(r'<figure class="wr-review-media".*?<img src="([^"]+)"', html)
        self.assertEqual(inline_sources, [f"posts/god-of-war-ragnarok/{filename}" for filename in assets])
        self.assertNotIn("Capturas de tela", html)
        self.assertEqual(html.count('class="wr-review-media"'), 3)

    def test_english_article_has_same_media_count(self):
        for slug, count in (("p4g", 4), ("god-of-war-ragnarok", 3)):
            with self.subTest(slug=slug):
                post = build.load_post(slug)
                html = build.article(post, "en")
                self.assertEqual(html.count('class="wr-review-media"'), count)
                self.assertNotIn("Screenshots", html)


if __name__ == "__main__":
    unittest.main()

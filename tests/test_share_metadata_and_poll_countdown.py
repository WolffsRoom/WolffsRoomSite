"""Social previews use real post paths; countdown follows Brazil poll close time."""
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build


class SocialShareAndCountdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.posts, cls.order = build.load_all()

    def test_home_og_cover_and_per_post_path(self):
        source = (ROOT / "tools/template.html").read_text(encoding="utf8")
        self.assertIn('<!--OGURL-->', source)
        self.assertIn('<!--OGIMAGE-->', source)
        self.assertIn('summary_large_image', source)
        self.assertIn('og:image:secure_url', source)
        self.assertIn('og:image:type', source)
        builder = (ROOT / 'tools/build.py').read_text('utf8')
        self.assertIn("cover_version = hashlib.sha256", builder)
        self.assertIn("'assets/CapaSite.png?v=' + cover_version",builder)
        self.assertIn("data-wr-poll-countdown", source)
        self.assertIn("setInterval(refreshPollCountdowns, 30000)", source)
        self.assertTrue((ROOT / "assets/CapaSite.png").is_file())
        builder = (ROOT / "tools/build.py").read_text(encoding="utf8")
        self.assertIn("SITE_URL + 'assets/CapaSite.png?v=' + cover_version", builder)
        self.assertIn("write_share_pages(posts)", builder)
        self.assertIn('rootPath + \'posts/\'', source)
        self.assertIn('location.pathname.match', source)

    def test_specific_post_has_social_og_and_redirect(self):
        with tempfile.TemporaryDirectory() as td:
            old = build.OUT
            try:
                build.OUT = td
                build.write_share_pages({
                    key: self.posts[key] for key in
                    ("next-vita-project-poll", "youtube-on-vita")
                })
            finally:
                build.OUT = old
            for slug in ("next-vita-project-poll", "youtube-on-vita"):
                page = (Path(td) / "posts" / slug / "index.html").read_text("utf8")
                cover = self.posts[slug]["cover"]
                self.assertIn(f'content="https://wolffsroom.github.io/WolffsRoomSite/{cover}"', page)
                self.assertIn(f'content="https://wolffsroom.github.io/WolffsRoomSite/posts/{slug}/"', page)
                self.assertIn(f'location.replace("https://wolffsroom.github.io/WolffsRoomSite/#{slug}")', page)
                self.assertIn('name="twitter:card" content="summary_large_image"', page)
                self.assertNotIn('http-equiv="refresh"', page)

    def test_closed_poll_has_bilingual_results_instead_of_countdown(self):
        p = self.posts["next-vita-project-poll"]
        pt = build.poll_article(p, "pt")
        en = build.poll_article(p, "en")
        for html in (pt, en):
            self.assertNotIn('data-wr-poll-countdown', html)
            self.assertIn('84%',html)
            self.assertIn('wr-poll-options',html)
        self.assertIn('Enquete encerrada.',pt)
        self.assertIn('Poll closed.',en)


if __name__ == "__main__":
    unittest.main()

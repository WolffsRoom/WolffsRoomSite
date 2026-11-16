"""Translation Details and percentage-based colors stay aligned with the Vita app."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build

class TranslationDetailsTests(unittest.TestCase):
    def test_va11_translation_details_in_both_languages(self):
        p = build.load_post("va-11-hall-a-ptbr")
        labels = [key for key, _ in p["meta"]]
        self.assertEqual(labels, ["Lançamento", "Desenvolvedor", "Versão",
                                  "Plataformas", "Ferramentas usadas"])
        self.assertIn("21 de junho de 2016", p["meta"][0][1])
        self.assertEqual(p["meta"][2][1], "PCSE00756 (USA)")
        self.assertIn("Undertale Mod Tool", p["meta"][-1][1])
        self.assertEqual([key for key, _ in p["en"]["meta"]][-1], "Tools used")
        self.assertEqual([key for key, _ in p["en"]["meta"]][0], "Release date")
        self.assertEqual([key for key, _ in p["sources"]], ["Tradução base (PC)"])
        raw = (ROOT / "content/posts/va-11-hall-a-ptbr/post.md").read_text("utf-8")
        self.assertNotIn("wolffsroom.wordpress.com", raw)
        self.assertEqual(p["date"].isoformat(), "2025-01-12")
        self.assertEqual(p["news_kind"], "")

    def test_color_at_thresholds(self):
        for pct, expected in [(0, "#e05a5a"),(20, "#e05a5a"),(39, "#e05a5a"),
                              (40, "#f4c430"),(69, "#f4c430"),(79, "#f4c430"),
                              (80, "#52c98c"),(100, "#52c98c")]:
            with self.subTest(pct=pct):
                self.assertEqual(build.progress_color(pct), expected)
                self.assertIn("--wr-progress-color: " + expected, build.bar("test", pct))
        css = (ROOT / "tools/template.html").read_text("utf-8")
        self.assertIn("var(--wr-progress-color,#ffffff)", css)

if __name__ == "__main__":
    unittest.main()

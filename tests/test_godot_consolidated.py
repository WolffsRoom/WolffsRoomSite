"""One Godot post serves the site and Vita, preserving the v0.3 showcase."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build

class GodotConsolidatedTests(unittest.TestCase):
    def test_canonical_post_and_original_deep_link(self):
        posts, order = build.load_all()
        self.assertIn("godot", posts)
        self.assertNotIn("godot-v03", posts)
        godot = posts["godot"]
        self.assertEqual(godot["cat"], "ferramentas")
        self.assertEqual(godot["subcat"], "ferramentas")
        self.assertFalse(godot["home_allowed"])
        self.assertEqual(godot["date"].isoformat(), "2026-06-05")
        self.assertEqual(godot["updated"].isoformat(), "2026-11-13")
        self.assertEqual(len(godot["downloads"]), 1)
        self.assertIn("Godot4Vita-v0.3-Showcase.vpk", godot["downloads"][0]["url"])
        self.assertIn("libgodot.so", " ".join(x for sec in godot["secs"] for x in sec["items"]))
        self.assertIn("GXM", " ".join(x for sec in godot["secs"] for x in sec["items"]))
        self.assertTrue((ROOT / "content/posts/godot/capa.png").stat().st_size > 1000)
        self.assertTrue((ROOT / "content/posts/godot/logo-original.png").stat().st_size > 1000)
        self.assertIn("posts/godot/logo-original.png", godot["shots"])
        template = (ROOT/"tools/template.html").read_text("utf-8")
        self.assertIn("if (h === 'godot-v03') h = 'godot'", template)

if __name__=="__main__":
    unittest.main()

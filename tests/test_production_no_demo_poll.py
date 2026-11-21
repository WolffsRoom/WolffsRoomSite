"""Production must never ship a demo ballot or experimental vote endpoint."""
import unittest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import build,store

class NoFakePollProductionTests(unittest.TestCase):
 def test_only_real_polls_from_content(self):
  posts,order=build.load_all()
  self.assertNotIn("enquete-demo-local",posts)
  self.assertNotIn("enquete-demo-local",order)
  self.assertEqual(len(posts), len(list((ROOT / "content/posts").glob("*/post.md"))))
  self.assertTrue(posts["next-vita-project-poll"].get("poll"))
  self.assertIn(build.choose_feature(posts,order), ("next-vita-project-poll", "youtube-on-vita"))

 def test_no_demo_script_or_fake_post_in_production(self):
  template=(ROOT/"tools/template.html").read_text("utf-8")
  source=(ROOT/"tools/build.py").read_text("utf-8")
  self.assertNotIn("enquete-demo-local",template+source)
  self.assertNotIn("WOLFFS_LOCAL_POLL_DEMO",template+source)
  self.assertFalse((ROOT/"preview-only").exists())
  self.assertIn("wr-deck-stage",template)
  self.assertIn("wr-filter-panel",template)
  self.assertNotIn("wr-foot-pixel-scene",template)
  self.assertIn("wr-foot-dither",template)
  self.assertIn(".wr-poll-detail>.wr-poll-back",template)

 def test_english_poll_translation_framework_exists(self):
  source=(ROOT/"tools/build.py").read_text("utf-8")
  self.assertIn("def poll_heading(",source)
  self.assertIn("poll_question",source)
  self.assertIn("poll_options",source)
  self.assertIn("def poll_article(",source)
  self.assertIn('data-act="openVita"',source)
  self.assertNotIn('data-act="sendVote"',source)

if __name__=="__main__":
 unittest.main()

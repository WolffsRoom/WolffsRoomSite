"""Pokémon Emerald 3D Voxel v0.5.8 development-news regression tests."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import build

SLUG="pokemon-emerald-voxel-ptbr-058"

class PokemonV058NewsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.news=build.load_post(SLUG)

 def test_news_is_unreleased_not_a_download(self):
  n=self.news
  self.assertEqual(n["cat"],"journal")
  self.assertEqual(n["subcat"],"news")
  self.assertEqual(n["group"],"Em andamento")
  self.assertEqual(n["date"].isoformat(),"2026-11-20")
  self.assertEqual(n["version_label"],"v0.5.8")
  self.assertNotEqual(n["news_kind"],"Release")
  self.assertFalse(n["downloads"])
  self.assertIn("ainda não disponível",n["status"])

 def test_bilingual_article_and_original_screenshot(self):
  n=self.news
  image=ROOT/"content/posts"/SLUG/"capa.png"
  self.assertTrue(image.is_file())
  self.assertEqual(n["cover"],"posts/"+SLUG+"/capa.png")
  self.assertIn("posts/"+SLUG+"/capa.png",n["shots"])
  en=build.news_article(n,"en")
  pt=build.news_article(n,"pt")
  self.assertIn("Pokémon Emerald 3D Voxel",pt)
  self.assertIn("v0.5.8",en)
  self.assertIn("v0.5.8",pt)
  self.assertIn('capa.png',en)
  self.assertIn('capa.png',pt)

if __name__=="__main__":
 unittest.main()

"""News text preserves separate PT-BR and English paragraphs in rendered HTML."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build

class NewsParagraphSpacing(unittest.TestCase):
 def test_paragraphs_preserved_across_languages(self):
  p=build.load_post('youtube-on-vita-updates-news')
  for lang in ('pt','en'):
   text=build.V(p,lang)['about']
   self.assertEqual(len(text.split('\n\n')),5)
   html=build.article(p,lang)
   self.assertEqual(html.count('margin:0 0 20px;color:#e0e0e0'),5)
  self.assertIn('conforme ilustro na imagem',build.article(p,'pt'))
  self.assertIn('as shown in the screenshot',build.article(p,'en'))

if __name__=='__main__':
 unittest.main()

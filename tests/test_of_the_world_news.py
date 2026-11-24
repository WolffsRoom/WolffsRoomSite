import sys
import unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build

class OfTheWorldNewsTests(unittest.TestCase):
    def test_news_is_bilingual_with_real_images(self):
        p=build.load_post('of-the-world-psvita-wip')
        self.assertEqual(p['subcat'],'news')
        self.assertIn('[WIP] Of the World',p['title'])
        self.assertIn('widescreen',p['about'].lower())
        self.assertEqual([Path(s).name for s in p['shots']],['Print1.jpg','Print2.jpg'])
        self.assertEqual(Path(p['cover']).name,'CapaNewsOTW.png')
        self.assertIn('playable beta',p['en']['about'].lower())
        self.assertIn('Temmie',p['en']['about'])
        for f in ('CapaNewsOTW.png','Print1.jpg','Print2.jpg'):
            with Image.open(ROOT/'content/posts/of-the-world-psvita-wip'/f) as im:
                im.verify()
        en=build.news_article(p,'en')
        pt=build.news_article(p,'pt')
        for html in (en,pt):
            self.assertIn('Print1.jpg',html)
            self.assertIn('Print2.jpg',html)
        self.assertIn('Forte abraço',pt)
        self.assertIn('Take care',en)

if __name__=='__main__':
    unittest.main()

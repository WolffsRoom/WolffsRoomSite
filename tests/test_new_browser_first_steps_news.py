import sys
import unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build

class BrowserFirstStepsNewsTests(unittest.TestCase):
    def test_news_content_and_images(self):
        item=build.load_post('new-browser-for-vita-first-steps-news')
        self.assertEqual(item['subcat'],'news')
        self.assertEqual(item['title'],'[WIP] New Browser for Vita - Firsts steps')
        self.assertEqual(Path(item['cover']).name,'Capa.png')
        self.assertEqual([Path(img).name for img in item['shots']],['Wikipedia.png'])
        self.assertIn('Cobalt 27',item['about']+' '+str(item['secs']))
        self.assertIn('Chromium M138',str(item['secs']))
        self.assertIn('Firewolff',str(item['secs']))
        self.assertIn('Vita3K',str(item['secs']))
        en=build.news_article(item,'en')
        pt=build.news_article(item,'pt')
        for html in (en,pt):
            self.assertIn('Wikipedia.png',html)
        self.assertIn('Cheers!',en)
        self.assertIn('Valeu!',pt)
        for name in ('Capa.png','Wikipedia.png'):
            with Image.open(ROOT/'content/posts/new-browser-for-vita-first-steps-news'/name) as im:
                im.verify()

if __name__=='__main__':
    unittest.main()

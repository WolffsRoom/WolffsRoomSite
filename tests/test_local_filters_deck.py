"""Checks for the isolated original-layout filters and overlapping deck."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build


class LocalFiltersDeckTests(unittest.TestCase):
    def setUp(self):
        self.posts, self.order = build.load_all()

    def test_filters_for_all_categories_and_return_at_bottom(self):
        html = build.lists_html(self.posts, self.order)
        for cat, keys in {
            'ports': ['Finalizado', 'Em andamento', 'Próximos', 'Outras equipes'],
            'ferramentas': ['apps', 'ferramentas', 'modificacoes', 'plugins'],
            'traducoes': build.GROUPS,
            'journal': ['news', 'reviews', 'enquetes'],
        }.items():
            self.assertIn('data-wr-filter-cat="'+cat+'" data-wr-filter-key="all"', html)
            for key in keys:
                self.assertIn('data-wr-filter-cat="'+cat+'" data-wr-filter-key="'+key+'"', html)
                self.assertIn('data-wr-section-cat="'+cat+'" data-wr-section-key="'+key+'"', html)
            start = html.index('<section aria-label="' + build.UI['en']['cats'][cat] + '"')
            end = html.index('</section>', start)
            fragment = html[start:end]
            self.assertIn("wr-category-back", fragment)
            self.assertEqual(fragment.count('data-act="goHome"'), 1)
            self.assertGreater(fragment.find('data-act="goHome"'),
                               fragment.find('data-wr-section-cat="'+cat+'"'))

    def test_three_latest_cards_followed_by_older_carousel(self):
        html = build.home_html(self.posts, self.order, build.choose_feature(self.posts, self.order), [])
        self.assertIn('wr-latest-three-grid', html)
        self.assertIn('class="wr-other-releases"', html)
        self.assertIn('Outros lançamentos', html)
        self.assertIn('Other releases', html)
        self.assertIn('data-deck-dir="-1"', html)
        self.assertIn('data-deck-dir="1"', html)
        self.assertIn('class="wr-explore-prompt"', html)
        chronological = [k for k in self.order if not self.posts[k].get('poll')]
        latest = html[html.index('class="wr-grid wr-latest-three-grid"'):
                      html.index('class="wr-other-releases"')]
        deck = html[html.index('class="wr-other-releases"'):
                    html.index('class="wr-explore-prompt"')]
        for slug in chronological[:3]:
            self.assertIn('data-act="open_'+slug+'"', latest)
            self.assertNotIn('data-act="open_'+slug+'"', deck)
        for slug in chronological[3:15]:
            self.assertIn('data-act="open_'+slug+'"', deck)
        self.assertEqual(latest.count('class="wr-card '), 3)
        self.assertEqual(deck.count('class="wr-deck-card"'), 12)
        ranks = re.findall(r'class="wr-deck-card"[^>]*data-deck-rank="([0-9]+)"', deck)
        self.assertEqual(ranks[:5], ['1','2','3','4','5'])
        template = (ROOT/'tools/template.html').read_text('utf-8')
        self.assertIn('var deckCenter = 0;', template)
        self.assertIn('const debut = {0:0, 1:1, 2:-1, 3:-2, 4:2}', template)
        self.assertLess(html.index('class="wr-grid wr-latest-three-grid"'),
                        html.index('class="wr-other-releases"'))
        self.assertLess(html.index('class="wr-other-releases"'),
                        html.index('class="wr-explore-prompt"'))
        self.assertLess(html.index('class="wr-explore-prompt"'),
                        html.index('class="wr-nav"'))

    def test_actions_and_hover_lift_only_in_template(self):
        template = (ROOT/'tools/template.html').read_text('utf-8')
        for part in ('[data-wr-filter-cat]', '[data-wr-section-cat]',
                     'data-wr-pos="away"', 'data-deck-dir', 'function moveDeck(dir)',
                     'translateY(-20px) scale(1.04)', 'aria-pressed'):
            self.assertIn(part, template)
        self.assertIn('data-wr-pos="0"', template)
        self.assertIn('data-wr-pos="-2"', template)
        self.assertIn('data-wr-pos="2"', template)

    def test_outer_cards_never_expand_to_full_size_or_steal_focus(self):
        template=(ROOT/'tools/template.html').read_text('utf-8')
        self.assertNotIn('.wr-deck-card:not([data-wr-pos="away"]):hover', template)
        self.assertIn('left:16%;z-index:2;transform:translateX(-50%) scale(.69)',template)
        self.assertIn('left:84%;z-index:2;transform:translateX(-50%) scale(.69)',template)
        self.assertIn('left:32%;z-index:4;transform:translateX(-50%) scale(.86)',template)
        self.assertIn('left:68%;z-index:4;transform:translateX(-50%) scale(.86)',template)
        self.assertIn('translateY(-6px) scale(.70)',template)
        self.assertIn('translateY(-10px) scale(.86)',template)
        self.assertIn('window.matchMedia(\'(max-width: 520px)\')',template)
        self.assertIn("window.addEventListener('resize', drawDeck",template)
        self.assertIn("var limit = narrow ? 1 : 2;",template)


if __name__=='__main__':
    unittest.main()

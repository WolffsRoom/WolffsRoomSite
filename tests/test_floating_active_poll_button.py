"""The floating active-poll shortcut mirrors the PS Vita shortcut."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build

class ActivePollShortcutTests(unittest.TestCase):
    def test_icon_is_bundled_and_shortcut_is_positioned_above_vita(self):
        self.assertTrue((ROOT/'assets/polls/CaixaWhite.png').is_file())
        source=(ROOT/'tools/template.html').read_text('utf8')
        self.assertLess(source.index('<!--ACTIVEPOLLBTN-->'),
                        source.index('<button class="wr-vitabtn"'))
        self.assertIn('bottom:244px;right:16px',source)
        self.assertIn('.wr-vitabtn{position:fixed;bottom:168px',source)
        self.assertIn('.wr-poll-float[hidden]{display:none!important}',source)
        self.assertIn('refreshActivePollButton()',source)
        self.assertIn('from <= now && now < until',source)

    def test_button_targets_actual_configured_poll(self):
        posts,order=build.load_all()
        html=build.floating_poll_buttons(posts,order)
        self.assertIn('data-act="open_next-vita-project-poll"',html)
        self.assertIn('href="https://wolffsroom.github.io/WolffsRoomSite/posts/next-vita-project-poll/"',html)
        self.assertIn('data-poll-end="2026-11-23T22:25:00-03:00"',html)
        self.assertIn('assets/polls/CaixaWhite.png',html)
        self.assertIn('hidden>',html)

    def test_non_poll_articles_do_not_generate_buttons(self):
        posts,order=build.load_all()
        ordinary={slug:posts[slug] for slug in order if not posts[slug].get('poll')}
        self.assertEqual(build.floating_poll_buttons(ordinary,list(ordinary)),'')


if __name__=='__main__':
    unittest.main()

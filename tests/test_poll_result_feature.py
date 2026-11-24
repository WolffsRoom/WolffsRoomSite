import datetime as dt
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import build

class PollResultFeatureTests(unittest.TestCase):
    def test_result_shows_for_one_day_only(self):
        tz=dt.timezone(dt.timedelta(hours=-3))
        result=build.load_post('next-vita-project-poll-result')
        prior=build.load_post('youtube-on-vita')
        posts={result['slug']:result,prior['slug']:prior}
        order=list(posts)
        before=dt.datetime(2026,11,23,22,40,tzinfo=tz)
        during=dt.datetime(2026,11,24,12,0,tzinfo=tz)
        after=dt.datetime(2026,11,24,22,42,tzinfo=tz)
        self.assertNotEqual(build.choose_feature(posts,order,before),result['slug'])
        self.assertEqual(build.choose_feature(posts,order,during),result['slug'])
        self.assertNotEqual(build.choose_feature(posts,order,after),result['slug'])
    def test_centered_result_chart_and_cover(self):
        item=build.load_post('next-vita-project-poll-result')
        en=build.news_article(item,'en')
        pt=build.news_article(item,'pt')
        for html in (en,pt):
            self.assertIn('class="wr-result-cover"',html)
            self.assertIn('posts/next-vita-project-poll-result/capa.png',html)
            self.assertIn('class="wr-result-chart"',html)
            self.assertIn('class="wr-result-track"',html)
            self.assertIn('New Browser for Vita',html)
            self.assertNotIn('Total votes: 19',html)
            self.assertNotIn('Total de votos: 19',html)
        self.assertIn('16 votes',en)
        self.assertIn('84.21%',en)
        self.assertIn('1 vote',en)
        self.assertIn('5.26%',en)

    def test_official_vote_counts(self):
        import json
        p=Path(__file__).resolve().parents[1]/'content/poll-results/next-vita-project-poll.json'
        data=json.loads(p.read_text(encoding='utf-8'))
        self.assertEqual(data['counts'],[16,1,1,1])
        self.assertEqual(sum(data['counts']),19)

if __name__=='__main__':
    unittest.main()

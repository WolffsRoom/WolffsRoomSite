"""Downloads are sums of GitHub release assets, never fabricated counts."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build,store


class GitHubDownloadTotals(unittest.TestCase):
    def test_counts_across_releases_and_ignores_drafts(self):
        releases=[
            {'draft':False,'assets':[{'download_count':9},{'download_count':11}]},
            {'draft':True,'assets':[{'download_count':500}]},
            {'draft':False,'assets':[{'download_count':4}]}
        ]
        with patch.object(store,'_api',return_value=releases) as api:
            self.assertEqual(store.github_total_downloads('WolffsRoom/Test'),24)
            api.assert_called_once_with('/repos/WolffsRoom/Test/releases?per_page=100&page=1')

    def test_unavailable_data_is_not_zero(self):
        with patch.object(store,'_api',return_value=None):
            self.assertIsNone(store.github_total_downloads('WolffsRoom/Test'))
        with patch.object(store,'_api',return_value=[{'assets':[{}]}]):
            self.assertIsNone(store.github_total_downloads('WolffsRoom/Test'))

    def test_repo_per_project_not_unrelated_links(self):
        posts,_=build.load_all()
        self.assertEqual(store.github_project_repo(posts['youtube-on-vita']),
                         'WolffsRoom/YouTubeOnVita')
        self.assertEqual(store.github_project_repo(posts['dd-touchonvita']),
                         'WolffsRoom/DD-TouchOnVita')
        self.assertIsNone(store.github_project_repo(posts['pokemon-emerald']))

    def test_shows_between_downloads_and_details(self):
        posts,_=build.load_all()
        p=posts['youtube-on-vita']
        p['github_downloads_total']=12345
        pt=build.article(p,'pt')
        en=build.article(p,'en')
        self.assertIn('Total de downloads',pt)
        self.assertIn('Total downloads',en)
        self.assertIn('12.345',pt)
        self.assertTrue(pt.index('wr-gh-download-count') > pt.index('Downloads'))
        self.assertTrue(pt.index('wr-gh-download-count') < pt.index('Detalhes'))
        p['github_downloads_total']=None
        self.assertNotIn('wr-gh-download-count',build.article(p,'en'))


if __name__=='__main__':
    unittest.main()

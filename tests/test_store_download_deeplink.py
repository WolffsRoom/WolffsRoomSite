"""Shareable Store download modal shortcut: no intro or navigation side effects."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build


class StoreDownloadDeepLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=(ROOT/'tools/template.html').read_text(encoding='utf8')

    def test_query_opens_existing_store_modal_on_boot(self):
        src=self.template
        self.assertIn("new URLSearchParams(location.search).get('download') === 'store'",src)
        self.assertIn("if (storeDownloadRequested()) comp.state.vitaOpen = true;",src)
        self.assertIn("if (!atHome || st.vitaOpen) { this.start(true); return; }",src)
        self.assertIn('data-if="vitaOpen"',build.vita_modal())
        self.assertIn('Baixar VPK',build.vita_modal())
        self.assertIn('Download VPK',build.vita_modal())

    def test_closing_modal_removes_deep_link_parameter(self):
        src=self.template
        self.assertIn("url.searchParams.delete('download');",src)
        self.assertIn("history.replaceState(null, '', url.pathname + url.search + url.hash);",src)
        self.assertEqual(src.count("clearStoreDownloadLink();"),2)
        self.assertIn('self.setState({ vitaOpen: false, qrOpen: false });',src)

    def test_original_site_navigation_is_preserved(self):
        src=self.template
        self.assertIn("function stateFromHash()",src)
        self.assertIn("location.pathname.match(/\\/posts\\/([a-z0-9-]+)\\/?$/)",src)
        self.assertIn('data-act="openVita"',src)


if __name__=='__main__':
    unittest.main()

"""GameLab translation names and responsive download mirror prioritization."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build
import store

TARGETS = {
    "wolf": ("The Wolf Among Us (PTBR)", "PCSE00352", "15wPBd36wCPJnXkCQxTQ8Kk_lovv4AU-p"),
    "twd1": ("The Walking Dead: Temporada 1 (PTBR)", "PCSE00316", "1XNHD9ruQsComRdrR3jnbu4yGVJJS9ErU"),
    "twd2": ("The Walking Dead: Temporada 2 (PTBR)", "PCSE00556", "1_U2kVFTmZ0uiHE1s2I9BHViSMlbhrCGw"),
}

class GameLabDownloadTests(unittest.TestCase):
    def test_site_download_metadata(self):
        for slug, (name, tid, drive_id) in TARGETS.items():
            with self.subTest(slug=slug):
                post = build.load_post(slug)
                download = post["downloads"][0]
                self.assertEqual(download["nome"], name)
                self.assertEqual(download["tipo"], "traducao")
                self.assertEqual(download["titleids"], [tid])
                self.assertEqual(download["senha"], "wolffsroom")
                self.assertEqual(download["app_min"], "1.0")
                self.assertIn(drive_id, download["url"])
                self.assertIn("drive.google.com", download["url"])
                self.assertIn("mediafire.com/file/", download["alternativas"][0])
                self.assertIn("mega.nz/file/", download["alternativas"][1])

    def test_new_client_gets_one_correctly_named_install_per_post(self):
        posts = {slug: build.load_post(slug) for slug in TARGETS}
        with TemporaryDirectory() as output:
            with patch.object(store, "app_release", return_value=None):
                store.write_store(posts, list(posts), "wolf", build.GROUPS, output)
            old = json.loads((Path(output) / "store.json").read_text("utf-8"))
            new = json.loads((Path(output) / "store-v1.json").read_text("utf-8"))
            for post in old["posts"]:
                self.assertEqual(post["downloads"], [])
            for post in new["posts"]:
                name, tid, drive_id = TARGETS[post["slug"]]
                self.assertEqual(len(post["downloads"]), 1)
                item = post["downloads"][0]
                self.assertEqual(item["nome"], name)
                self.assertEqual(item["titleids"], [tid])
                self.assertIn("drive.usercontent.google.com/download", item["url"])
                self.assertIn(drive_id, item["url"])
                self.assertIn("mediafire.com/file/", item["alternativas"][0])

if __name__ == "__main__":
    unittest.main()

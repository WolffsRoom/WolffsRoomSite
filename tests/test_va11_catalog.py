"""Original VA-11 post stays dated 2025 and protected until the Vita v1.0 release."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build
import store

class VA11StoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = build.load_post("va-11-hall-a-ptbr")

    def test_original_date_and_not_a_new_release(self):
        p = self.p
        self.assertEqual(p["date"].isoformat(), "2025-01-12")
        self.assertEqual(p["news_kind"], "")
        self.assertEqual(len(p["shots"]), 5)
        self.assertEqual(len(p["links"]), 3)

    def test_single_translation_with_fallback_and_password(self):
        d = self.p["downloads"]
        self.assertEqual(len(d), 1)
        self.assertEqual(d[0]["titleids"], ["PCSE00756"])
        self.assertEqual(d[0]["senha"], "wolffsroom")
        self.assertEqual(len(d[0]["alternativas"]), 2)

    def test_old_app_cannot_accidentally_install_aes_patch(self):
        with TemporaryDirectory() as out:
            with patch.object(store, "app_release", return_value=None):
                store.write_store({self.p["slug"]: self.p}, [self.p["slug"]],
                                  self.p["slug"], build.GROUPS, out)
            data = json.loads((Path(out) / "store.json").read_text("utf-8"))
            item = data["posts"][0]
            self.assertEqual(item["data"], "2025-01-12")
            self.assertEqual(len(item["downloads"]), 0)
            self.assertEqual(len(item["pt"]["links"]), 3)

    def test_future_app_gets_one_install_with_two_mirrors(self):
        p = dict(self.p)
        p["downloads"] = [dict(self.p["downloads"][0], app_pendente=False)]
        with TemporaryDirectory() as out:
            with patch.object(store, "app_release", return_value=None):
                store.write_store({p["slug"]: p}, [p["slug"]],
                                  p["slug"], build.GROUPS, out)
            data = json.loads((Path(out) / "store.json").read_text("utf-8"))
            ds = data["posts"][0]["downloads"]
            self.assertEqual(len(ds), 1)
            self.assertEqual(ds[0]["tipo"], "traducao")
            self.assertEqual(ds[0]["senha"], "wolffsroom")
            self.assertEqual(len(ds[0]["alternativas"]), 2)

if __name__ == "__main__":
    unittest.main()

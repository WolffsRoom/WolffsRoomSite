"""The PS Vita store.json carries the same per-post dates used by site Details."""
import datetime
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("site_store", ROOT / "tools" / "store.py")
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)

def a_post(updated):
    return {
        "cat": "ports", "group": "Finalizado", "date": datetime.date(2026, 11, 15),
        "updated": updated, "en": None, "pixel": False, "progress": 100,
        "cover": None, "shots": [], "video": None, "video_file": None,
        "trophies": False, "author": "", "author_url": "",
        "news_kind": "", "downloads": [], "links": [], "sources": [],
    }

class StorePostDateTests(unittest.TestCase):
    def render(self, updated):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(store, "_texts", return_value={}):
                with patch.object(store, "app_release", return_value=None):
                    store.write_store({"example": a_post(updated)}, ["example"], "example",
                                      ["Finalizado"], tmp)
            data = json.loads((Path(tmp) / "store.json").read_text("utf-8"))
            return data["posts"][0]

    def test_published_and_updated_are_own_fields(self):
        item = self.render(datetime.date(2026, 11, 16))
        self.assertEqual(item["data"], "2026-11-15")
        self.assertEqual(item["atualizado_em"], "2026-11-16")

    def test_unmodified_post_hides_optional_update(self):
        self.assertEqual(self.render(None)["atualizado_em"], "")

if __name__ == "__main__":
    unittest.main()

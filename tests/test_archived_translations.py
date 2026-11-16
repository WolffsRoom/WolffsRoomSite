"""Historical translation catalog: dates, metadata, mirrors and safe installation gating."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build
import store

EXPECTED = {
    "delta1": ("2025-02-06", "Finalizado", "PCSB00964"),
    "cave": ("2025-02-06", "Finalizado", "DOKU41220"),
    "icono": ("2025-01-25", "Finalizado", "PCSE01177"),
    "va-11-hall-a-ptbr": ("2025-01-12", "Finalizado", "PCSE00756"),
    "wolf": ("2026-02-23", "Outras equipes", "PCSE00352"),
    "wipeout": ("2026-02-21", "Outras equipes", "PCSF00007"),
    "twd2": ("2026-02-18", "Outras equipes", "PCSE00556"),
    "twd1": ("2026-02-17", "Outras equipes", "PCSE00316"),
}

class ArchiveTranslationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.posts, _ = build.load_all()

    def test_original_dates_categories_and_no_new_release_badges(self):
        for slug, (date, group, _) in EXPECTED.items():
            with self.subTest(slug=slug):
                p = self.posts[slug]
                self.assertEqual(p["date"].isoformat(), date)
                self.assertEqual(p["group"], group)
                self.assertEqual(p["cat"], "traducoes")
                self.assertEqual(p["news_kind"], "")

    def test_all_details_end_with_tools_used(self):
        for slug, (_, _, titleid) in EXPECTED.items():
            with self.subTest(slug=slug):
                p = self.posts[slug]
                self.assertEqual(p["meta"][0][0], "Lançamento")
                self.assertEqual(p["en"]["meta"][0][0], "Release date")
                self.assertEqual(p["meta"][-1][0], "Ferramentas usadas")
                self.assertEqual(p["en"]["meta"][-1][0], "Tools used")
                self.assertTrue(any(titleid in str(value) for _, value in p["meta"]))

    def test_three_manual_mirrors_and_no_old_post_links(self):
        for slug in EXPECTED:
            with self.subTest(slug=slug):
                p = self.posts[slug]
                self.assertEqual(len(p["links"]), 3)
                self.assertEqual(len(p["en"].get("links") or p["links"]), 3)
                self.assertEqual({key.split()[0] for key, _ in p["links"]},
                                 {"Google", "MEGA", "MediaFire"})
                for lang in (p, {**p, **p["en"]}):
                    self.assertFalse(any("wolffsroom.wordpress.com" in url for _, url in lang["links"]))
                self.assertGreaterEqual(len(p["shots"]), 4)

    def test_correct_installation_package_and_password_in_staged_metadata(self):
        for slug, (_, _, titleid) in EXPECTED.items():
            with self.subTest(slug=slug):
                p = self.posts[slug]
                self.assertEqual(len(p["downloads"]), 1)
                d = p["downloads"][0]
                self.assertEqual(d["titleids"], [titleid])
                self.assertEqual(d["senha"], "wolffsroom")
                self.assertTrue(d["app_pendente"])
                self.assertEqual(len(d["alternativas"]), 2)
                self.assertEqual(len({d["url"], *d["alternativas"]}), 3)
                if slug in ("delta1", "cave"):
                    self.assertEqual(d["tipo"], "vpk")
                elif slug == "wipeout":
                    self.assertEqual(d["tipo"], "app_arquivos")
                else:
                    self.assertEqual(d["tipo"], "traducao")

    def test_old_vita_catalog_does_not_advertise_unverified_installers(self):
        posts = {slug: self.posts[slug] for slug in EXPECTED}
        with TemporaryDirectory() as out:
            with patch.object(store, "app_release", return_value=None):
                store.write_store(posts, list(EXPECTED), "delta1", build.GROUPS, out)
            data = json.loads((Path(out) / "store.json").read_text("utf-8"))
            for p in data["posts"]:
                self.assertEqual(p["downloads"], [])
                self.assertEqual(len(p["pt"]["links"]), 3)
                self.assertEqual(len(p["en"].get("links") or p["links"]), 3)

if __name__ == "__main__":
    unittest.main()

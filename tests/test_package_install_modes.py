"""Safe translation deployment: VPK archives, app-file patches, and old catalogs."""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build
import store

class PackageModesTests(unittest.TestCase):
    def test_deltarune_chapter_one_scripts_are_complete(self):
        p = build.load_post("delta1")
        self.assertEqual(p["date"].isoformat(), "2025-02-06")
        self.assertEqual(p["progress"], 100)
        self.assertEqual(p["status"], "100% · Disponível")
        self.assertEqual(p["en"]["status"], "100% · Available")
        self.assertEqual([b[1] for b in p["bars"]], [100, 100, 100, 100, 100])
        self.assertEqual([b[1] for b in p["en"]["bars"]], [100, 100, 100, 100, 100])
        self.assertEqual(len(p["shots"]), 5)
        self.assertTrue(p["shots"][-1].endswith(".gif"))
        self.assertEqual(p["downloads"][0]["tipo"], "vpk")
        self.assertEqual(p["downloads"][0]["arquivo"], "Deltarune PTBR.zip")
        self.assertEqual(p["downloads"][0]["senha"], "wolffsroom")

    def test_wipeout_uses_app_files_and_livearea_instructions(self):
        p = build.load_post("wipeout")
        d = p["downloads"][0]
        self.assertEqual(p["date"].isoformat(), "2026-02-21")
        self.assertEqual(d["tipo"], "app_arquivos")
        self.assertEqual(d["titleids"], ["PCSF00007"])
        self.assertEqual(d["senha"], "wolffsroom")
        self.assertTrue(d["app_pendente"])
        for lang in (p, p["en"]):
            content = str(lang["meta"]) + str(lang["secs"])
            self.assertIn("ux0:app/PCSF00007/", content)
            self.assertIn("FMVita", content)
            self.assertIn("File Manager", content)
            self.assertIn("torrent", content)

    def test_no_unverified_patch_reaches_public_old_app(self):
        posts = {slug: build.load_post(slug) for slug in ("delta1", "cave", "wipeout")}
        with TemporaryDirectory() as out:
            with patch.object(store, "app_release", return_value=None):
                store.write_store(posts, list(posts), "delta1", build.GROUPS, out)
            payload = json.loads((Path(out) / "store.json").read_text("utf-8"))
            for item in payload["posts"]:
                self.assertEqual(item["downloads"], [])
                self.assertEqual(len(item["pt"]["links"]), 3)

    def test_future_catalog_routes_vpk_and_app_files(self):
        posts = {slug: build.load_post(slug) for slug in ("delta1", "wipeout")}
        for p in posts.values():
            p["downloads"] = [dict(p["downloads"][0], app_pendente=False)]
        with TemporaryDirectory() as out:
            with patch.object(store, "app_release", return_value=None):
                store.write_store(posts, list(posts), "delta1", build.GROUPS, out)
            payload = json.loads((Path(out) / "store.json").read_text("utf-8"))
            data = {item["slug"]: item["downloads"] for item in payload["posts"]}
            self.assertEqual(data["delta1"][0]["tipo"], "vpk")
            self.assertEqual(data["delta1"][0]["arquivo"], "Deltarune PTBR.zip")
            self.assertEqual(data["wipeout"][0]["tipo"], "app_arquivos")
            self.assertEqual(data["wipeout"][0]["titleids"], ["PCSF00007"])
            self.assertEqual(data["wipeout"][0]["senha"], "wolffsroom")

if __name__ == "__main__":
    unittest.main()

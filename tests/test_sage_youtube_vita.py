"""Check SAGE 2019 v0.64 and YouTube on Vita v0.34 catalog integrity."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest,sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "tools"))
import build, store

class PostsTests(unittest.TestCase):
    def test_pizza_v064_keeps_existing_artwork_and_ids(self):
        p=build.load_post("pizza")
        self.assertEqual(p["version_label"], "v0.64")
        self.assertEqual(p["date"].isoformat(),"2026-11-14")
        self.assertEqual(p["cover"],"posts/pizza/capa.png")
        d=next(d for d in p["downloads"] if d["tipo"]=="vpk")
        self.assertEqual(d["tag"],"v0.64")
        self.assertEqual(d["titleids"],["PTSAGE001"])
        self.assertIn("v0.64",d["nome"])
        self.assertEqual(len(p["shots"]),6)
        content=" ".join(str(section) for section in p["secs"])
        self.assertIn("BC3",content)
        self.assertIn("obj_taunteffect",content)
        self.assertIn("analógico esquerdo",content)

    def test_youtube_v034_has_new_cover_shots_and_safeguards(self):
        p=build.load_post("youtube-on-vita")
        self.assertEqual(p["title"],"Youtube - Unofficial client for PS Vita (alpha)")
        self.assertEqual(p["cover"],"posts/youtube-on-vita/capa.png")
        self.assertEqual(len(p["shots"]),7)
        self.assertEqual(p["updated"].isoformat(),"2026-11-18")
        self.assertEqual(p["version_label"],"v0.34")
        d=p["downloads"][0]
        self.assertEqual(d["aviso_plugin"],"CapUnlocker")
        self.assertEqual(d["app_min"],"1.0.3")
        self.assertEqual(d["titleids"],["YTVCB0001"])
        self.assertTrue(d["url"].startswith("https://drive.google.com/file/d/"))
        self.assertNotIn("drive.google.com",str(p["links"]))
        en=build.V(p,"en")
        self.assertIn("Alpha status and limitations",str(en["secs"]))
        self.assertIn("60 fps",str(en["secs"]))
        self.assertIn("sign-in",str(en["secs"]).lower())

    def test_v103_feed_only_receives_youtube(self):
        posts={s:build.load_post(s) for s in ("pizza","youtube-on-vita")}
        with TemporaryDirectory() as out:
            with patch.object(store,"app_release",return_value=None):
                store.write_store(posts,list(posts),"youtube-on-vita",build.GROUPS,out)
            legacy=json.loads((Path(out)/"store.json").read_text("utf-8"))
            v1=json.loads((Path(out)/"store-v1.json").read_text("utf-8"))
            new=json.loads((Path(out)/"store-v103.json").read_text("utf-8"))
            for data in (legacy,v1):
                y=next(p for p in data["posts"] if p["slug"]=="youtube-on-vita")
                self.assertFalse(y["downloads"])
            y=next(p for p in new["posts"] if p["slug"]=="youtube-on-vita")
            self.assertEqual(len(y["downloads"]),1)
            d=y["downloads"][0]
            self.assertEqual(d["aviso_plugin"],"CapUnlocker")
            self.assertTrue(d["url"].startswith("https://drive.usercontent.google.com/download"))
            self.assertEqual(d["titleids"],["YTVCB0001"])

if __name__ == "__main__":
    unittest.main()

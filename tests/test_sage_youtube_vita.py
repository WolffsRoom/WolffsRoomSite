"""Check SAGE 2019 v0.64 and YouTube on Vita v0.65 release integrity."""
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

    def test_youtube_v065_release_has_updated_cover_shots_and_both_downloads(self):
        p=build.load_post("youtube-on-vita")
        self.assertEqual(p["title"],"YouTube on Vita")
        self.assertEqual(p["cover"],"posts/youtube-on-vita/release-v065.png")
        self.assertEqual(len(p["shots"]),12)
        self.assertEqual(p["updated"].isoformat(),"2026-11-22")
        self.assertEqual(p["version_label"],"v0.65")
        self.assertEqual(p["news_kind"],"Release")
        self.assertEqual(p["date"].isoformat(),"2026-11-17")
        self.assertEqual(len(p["downloads"]),2)
        self.assertEqual(
            [x["titleids"] for x in p["downloads"]],
            [["YTVCB0001"],["YTVCB0002"]])
        self.assertEqual([x["arquivo"] for x in p["downloads"]],
                         ["YouTube.vpk","YouTube-Lite.vpk"])
        self.assertTrue(all(x["app_min"] == "" for x in p["downloads"]))
        self.assertTrue(all(x["url"].startswith(
            "https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/")
            for x in p["downloads"]))
        self.assertEqual([x["tamanho"] for x in p["downloads"]],
                         [22923055,22923400])
        self.assertIn("YouTube Full", str(p["links"]))
        self.assertIn("YouTube Lite", str(p["links"]))
        en=build.V(p,"en")
        self.assertIn("What\'s new in v0.65",str(en["secs"]))
        self.assertIn("720p",str(en["secs"]))
        self.assertIn("sign-in",str(en["secs"]).lower())

    def test_all_store_feeds_receive_normal_and_lite_downloads(self):
        posts={s:build.load_post(s) for s in ("pizza","youtube-on-vita")}
        with TemporaryDirectory() as out:
            with patch.object(store,"app_release",return_value=None):
                store.write_store(posts,list(posts),"youtube-on-vita",build.GROUPS,out)
            for filename in ("store.json","store-v1.json","store-v103.json","store-v105.json"):
                data=json.loads((Path(out)/filename).read_text("utf-8"))
                y=next(p for p in data["posts"] if p["slug"]=="youtube-on-vita")
                self.assertTrue(y["destaque"])
                self.assertEqual(len(y["downloads"]),2)
                full,lite=y["downloads"]
                self.assertEqual(full["titleids"],["YTVCB0001"])
                self.assertEqual(lite["titleids"],["YTVCB0002"])
                self.assertEqual([x["arquivo"] for x in y["downloads"]],
                                 ["YouTube.vpk","YouTube-Lite.vpk"])
                self.assertEqual([x["tamanho"] for x in y["downloads"]],
                                 [22923055,22923400])
                self.assertTrue(all(
                    x["url"].startswith("https://github.com/WolffsRoom/YouTubeOnVita/releases/download/v0.65/")
                    for x in y["downloads"]))

if __name__ == "__main__":
    unittest.main()

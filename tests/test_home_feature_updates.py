"""Recent Updates/Releases drive both site and Vita home, not original post age."""
import datetime
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import build

D=datetime.datetime

def post(pub, activity, eligible=True):
    return {"when":pub,"activity_when":activity,"home_allowed":eligible}

class HomeFeatureUpdateTests(unittest.TestCase):
    def test_newer_update_beats_newer_original_publication(self):
        sample={
          "old-port":post(D(2026,6,1),D(2026,11,18,23,53)),
          "new-release":post(D(2026,11,18,23,32),D(2026,11,18,23,32)),
          "older-news":post(D(2026,11,17,9),D(2026,11,17,9)),
        }
        order=build.order_posts(sample)
        self.assertEqual(order,["old-port","new-release","older-news"])
        self.assertEqual(build.choose_feature(sample,order),"old-port")

    def test_historical_item_can_be_omitted_without_disappearing(self):
        sample={
          "archive":post(D(2020,1,1),D(2026,11,19,10),False),
          "sage":post(D(2026,11,14,17),D(2026,11,18,23,53)),
        }
        order=build.order_posts(sample)
        self.assertEqual(order[0],"archive")
        self.assertEqual(build.choose_feature(sample,order),"sage")

    def test_non_release_posts_do_not_claim_new_activity_by_source_edits(self):
        sample={
          "ordinary-old":post(D(2025,1,1),D(2025,1,1)),
          "sage":post(D(2026,11,14),D(2026,11,18,23,53)),
        }
        self.assertEqual(build.choose_feature(sample,build.order_posts(sample)),"sage")

    def test_youtube_first_release_becomes_feature_without_promoting_news(self):
        posts,order=build.load_all()
        # First public YouTube release now leads; Pokémon's update remains
        # available and Journal/News must not claim the launch slot.
        self.assertEqual(order[0],"next-vita-project-poll")
        self.assertIn("pokemon-emerald", order)
        self.assertIn("pokemon-emerald-voxel-ptbr-058", order)
        self.assertEqual(build.choose_feature(posts,order),"next-vita-project-poll")
        self.assertEqual(posts["youtube-on-vita"]["version_label"],"v0.58")
        self.assertEqual(posts["youtube-on-vita"]["news_kind"],"Release")
        self.assertEqual(posts["pokemon-emerald-voxel-ptbr-058"]["subcat"],"news")
        self.assertEqual(posts["pizza"]["news_kind"],"Update")
        self.assertEqual(posts["pizza"]["version_label"],"v0.64")
        self.assertGreater(posts["pizza"]["activity_when"],
                           posts["dd-touchonvita"]["activity_when"])
        self.assertEqual(posts["pizza"]["date"].isoformat(),"2026-11-14")
        self.assertEqual(posts["pizza"]["updated"].isoformat(),"2026-11-18")

    def test_manual_update_timestamp_and_home_opt_out(self):
        with tempfile.TemporaryDirectory() as tempdir:
            dest=Path(tempdir)/"youtube-on-vita"
            shutil.copytree(ROOT/"content/posts/youtube-on-vita",dest)
            p=dest/"post.md"
            content=p.read_text("utf-8")
            content,n=re.subn(r"^atualizado_em:.*$",
                "atualizado_em: '2026-11-18 14:25'\ndestaque_home: false",
                content,count=1,flags=re.MULTILINE)
            self.assertEqual(n,1)
            p.write_text(content,encoding="utf-8")
            with patch.object(build,"CONTENT",tempdir),patch.object(build,"post_last_commit_at",return_value=None):
                item=build.load_post("youtube-on-vita")
            self.assertEqual(item["activity_when"],D(2026,11,18,14,25))
            self.assertEqual(item["updated"],datetime.date(2026,11,18))
            self.assertFalse(item["home_allowed"])

    def test_git_commit_timestamp_respects_brazil_local_time(self):
        log="2026-11-19T02:53:54+00:00\n2026-11-14T20:59:00+00:00\n"
        with patch.object(build.subprocess,"check_output",return_value=log):
            actual=build.post_last_commit_at("pizza")
        self.assertEqual(actual,D(2026,11,18,23,53,54))

if __name__=="__main__":
    unittest.main()

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

    def test_youtube_release_update_becomes_feature_without_promoting_news(self):
        posts,order=build.load_all()
        # Updated YouTube release now leads; Pokémon's update remains
        # available and Journal/News must not claim the launch slot.
        self.assertIn("next-vita-project-poll", order)
        self.assertIn("pokemon-emerald", order)
        self.assertIn("pokemon-emerald-voxel-ptbr-058", order)
        self.assertIn(build.choose_feature(posts,order),("next-vita-project-poll","youtube-on-vita"))
        self.assertEqual(posts["youtube-on-vita"]["version_label"],"v0.65")
        self.assertEqual(posts["youtube-on-vita"]["news_kind"],"Release")
        self.assertEqual(posts["pokemon-emerald-voxel-ptbr-058"]["subcat"],"news")
        self.assertEqual(posts["pizza"]["news_kind"],"Update")
        self.assertEqual(posts["pizza"]["version_label"],"v0.64")
        self.assertGreater(posts["pizza"]["activity_when"],
                           posts["dd-touchonvita"]["activity_when"])
        self.assertEqual(posts["pizza"]["date"].isoformat(),"2026-11-14")
        self.assertEqual(posts["pizza"]["updated"].isoformat(),"2026-11-18")

    def test_home_recent_cards_exclude_main_feature_and_keep_order(self):
        posts = {
            "main": {"cat": "ferramentas", "poll": None},
            "second": {"cat": "ferramentas", "poll": None},
            "poll": {"cat": "journal", "poll": {"id": "poll"}},
            "third": {"cat": "ports", "poll": None},
            "news": {"cat": "journal", "poll": None},
            "fourth": {"cat": "ports", "poll": None},
        }
        order = ["main", "second", "poll", "third", "news", "fourth"]
        self.assertEqual(build.home_recent_posts(posts, order, "main"),
                         ["second", "third", "fourth"])
        self.assertEqual(build.home_recent_posts(posts, order, "poll"),
                         ["main", "second", "third", "fourth"])

    def test_latest_and_releases_localization(self):
        self.assertEqual(build.UI["pt"]["latest3"], "Confira também outras novidades...")
        self.assertEqual(build.UI["en"]["latest3"], "Check out more updates...")
        self.assertEqual(build.UI["pt"]["other_releases"], "Explore outros lançamentos")
        self.assertEqual(build.UI["en"]["other_releases"], "Explore other releases")

    def test_youtube_hero_description_localized_and_styled(self):
        posts, _ = build.load_all()
        post = posts["youtube-on-vita"]
        pt = build.V(post, "pt")["feature_text"]
        en = build.V(post, "en")["feature_text"]
        self.assertIn("Cliente não oficial", pt)
        self.assertIn("Unofficial YouTube client", en)
        self.assertIn("Full e Lite", pt)
        self.assertIn("Full and Lite", en)
        self.assertIn("<strong>", build.inline(en))
        self.assertIn("<em>", build.inline(en))
        self.assertIn("The real YouTube on TV experience", en)

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

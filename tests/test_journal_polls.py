import datetime
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import build,store

class JournalAndPollTests(unittest.TestCase):
 def test_existing_taxonomy(self):
  posts,order=build.load_all()
  expected={"darkest":"modificacoes","dd-touchonvita":"plugins",
    "fm":"apps","file-manager":"apps","shinokai":"apps",
    "youtube-on-vita":"apps","godot":"ferramentas",
    "ystool":"ferramentas","horizon":"modificacoes"}
  for slug,subcat in expected.items():
   self.assertEqual(posts[slug]["cat"],"ferramentas")
   self.assertEqual(posts[slug]["subcat"],subcat)
  for slug in ("p4g","god-of-war-ragnarok"):
   self.assertEqual(posts[slug]["cat"],"journal")
   self.assertEqual(posts[slug]["subcat"],"reviews")
  self.assertIn(build.choose_feature(posts,order), ("youtube-on-vita", "next-vita-project-poll"))

 def _fixture(self,td,now,days=None):
  f=Path(td)/"vote-test"
  f.mkdir()
  dur="" if days is None else "duracao_dias: "+str(days)+"\n"
  (f/"post.md").write_text(
   "---\ntitulo: Enquete Experimental\ncategoria: journal\nsubcategoria: enquetes\n"
   "grupo: Em andamento\ndata: '"+now.strftime("%Y-%m-%d %H:%M")+
   "'\nnovidade: ''\n"+dur+"opcoes:\n  - App Um\n  - App Dois\n  - App Três\n"
   "---\n\nEscolha um projeto.\n",encoding="utf-8")

 def test_three_days_and_preview_not_voting(self):
  now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
  with tempfile.TemporaryDirectory() as td:
   self._fixture(td,now)
   with patch.object(build,"CONTENT",td),patch.object(build,"post_last_commit_at",return_value=None):
    poll=build.load_post("vote-test")
   self.assertEqual(poll["poll"]["days"],3)
   self.assertEqual(len(poll["poll"]["options"]),3)
   self.assertEqual(datetime.datetime.fromisoformat(poll["poll"]["ends_at"])-
                    datetime.datetime.fromisoformat(poll["poll"]["starts_at"]),
                    datetime.timedelta(days=3))
   html=build.poll_article(poll,"pt")
   self.assertIn('data-act="openVita"',html)
   self.assertIn("Disponível somente pela loja",html)
   self.assertNotIn("Enviar resposta",html)
   # A poll post with a cover renders it centered above the options.
   poll["cover"] = "posts/vote-test/capa.png"
   html = build.poll_article(poll,"pt")
   self.assertIn('class="wr-poll-cover"',html)
   self.assertLess(html.index('class="wr-poll-cover"'),
                   html.index('class="wr-poll-options"'))

 def test_duration_home_first_day_only(self):
  now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
  with tempfile.TemporaryDirectory() as td:
   self._fixture(td,now,5)
   with patch.object(build,"CONTENT",td),patch.object(build,"post_last_commit_at",return_value=None):
    poll=build.load_post("vote-test")
   self.assertEqual(poll["poll"]["days"],5)
   posts,order=build.load_all()
   posts["vote-test"]=poll
   order=build.order_posts(posts)
   self.assertEqual(build.choose_feature(posts,order),"vote-test")
   poll["poll"]["starts_at"]=(now-datetime.timedelta(days=1)).replace(tzinfo=None).isoformat()
   poll["poll"]["ends_at"]=(now+datetime.timedelta(days=2)).replace(tzinfo=None).isoformat()
   self.assertEqual(build.choose_feature(posts,order),"next-vita-project-poll")

 def test_compact_news_media(self):
  posts,_=build.load_all()
  fixture=dict(posts["p4g"])
  fixture.update(cat="journal",subcat="news",news_kind="",
    shots=["posts/news/photo1.png"],video=None,video_file=None)
  text=build.news_article(fixture,"pt")
  self.assertIn("posts/news/photo1.png",text)
  self.assertIn("wr-journal-news",text)

 def test_feeds_subcategories_and_empty_backend(self):
  posts,order=build.load_all()
  with tempfile.TemporaryDirectory() as td:
   with patch.object(store,"app_release",return_value=None):
    with patch.dict(__import__("os").environ,{"WOLFFS_POLL_API_URL":""}):
     store.write_store(posts,order,build.choose_feature(posts,order),build.GROUPS,td)
   data=json.loads((Path(td)/"store-v105.json").read_text("utf-8"))
   self.assertEqual(data["enquetes_api"],"")
   self.assertEqual(next(p for p in data["posts"] if p["slug"]=="dd-touchonvita")["subcategoria"],"plugins")
   self.assertEqual(next(p for p in data["posts"] if p["slug"]=="p4g")["subcategoria"],"reviews")
   self.assertEqual([p["id"] for p in json.loads((Path(td)/"polls.json").read_text("utf-8"))["polls"]],["next-vita-project-poll"])

if __name__=="__main__":
 unittest.main()

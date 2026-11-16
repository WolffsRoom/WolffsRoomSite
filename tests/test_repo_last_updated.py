"""Dates belong to posts in Details; a site-wide footer date must not exist."""
import datetime
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("site_builder", ROOT / "tools" / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class PostDateTests(unittest.TestCase):
    def test_post_update_uses_only_its_own_git_history(self):
        log = "2026-11-16T13:57:22+00:00\n2026-11-14T12:00:00+00:00\n"
        with patch.object(build.subprocess, "check_output", return_value=log) as mocked:
            updated = build.post_last_updated("pokemon-emerald", datetime.date(2026, 11, 14))
        self.assertEqual(updated, datetime.date(2026, 11, 16))
        self.assertEqual(mocked.call_args.args[0][-2:], ["--", "content/posts/pokemon-emerald"])

    def test_first_commit_or_same_day_does_not_show_update(self):
        with patch.object(build.subprocess, "check_output",
                          return_value="2026-11-16T12:00:00+00:00\n"):
            self.assertIsNone(build.post_last_updated("new", datetime.date(2026, 11, 16)))
        with patch.object(build.subprocess, "check_output",
                          return_value="2026-11-16T13:00:00+00:00\n2026-11-15T12:00:00+00:00\n"):
            self.assertIsNone(build.post_last_updated("same-day", datetime.date(2026, 11, 16)))

    def test_language_dates_and_no_footer_marker(self):
        day = datetime.date(2026, 11, 16)
        self.assertIn("16/11/2026", build.post_date_html(day, "pt"))
        self.assertIn("November 16, 2026", build.post_date_html(day, "en"))
        self.assertNotIn("<!--LAST_UPDATED-->", (ROOT / "tools" / "template.html").read_text("utf-8"))
        self.assertNotIn("repo_last_updated()", (ROOT / "tools" / "build.py").read_text("utf-8"))

if __name__ == "__main__":
    unittest.main()

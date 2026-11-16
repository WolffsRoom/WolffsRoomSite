"""Footer should show repository commit time, not rebuild/current time."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("site_builder", ROOT / "tools" / "build.py")
# The normal build imports tools/store.py by adding its directory to sys.path.
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class LastUpdatedTests(unittest.TestCase):
    def test_git_commit_timestamp_in_both_languages(self):
        with patch.object(build.subprocess, "check_output",
                          return_value="2026-11-16T01:54:27-03:00\n") as mock:
            result = build.repo_last_updated()
        mock.assert_called_once()
        self.assertIn("git", mock.call_args.args[0])
        self.assertIn("Atualizado em: ", result)
        self.assertIn("16/11/2026", result)
        self.assertIn("Last update: ", result)
        self.assertIn("November 16, 2026", result)
        self.assertEqual(result.count('datetime="2026-11-16"'), 2)

    def test_date_follows_commit_not_build_clock(self):
        with patch.object(build.subprocess, "check_output",
                          return_value="2025-12-31T23:59:00-03:00\n"):
            result = build.repo_last_updated()
        self.assertIn("31/12/2025", result)
        self.assertIn("December 31, 2025", result)

    def test_template_contains_generated_marker(self):
        template = (ROOT / "tools/template.html").read_text("utf-8")
        self.assertEqual(template.count("<!--LAST_UPDATED-->"), 1)
        script = (ROOT / "tools/build.py").read_text("utf-8")
        self.assertIn("page.replace('<!--LAST_UPDATED-->', repo_last_updated())", script)


if __name__ == "__main__":
    unittest.main()

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pack  # noqa: E402

FM = "---\nname: {name}\ndescription: {desc}\nmetadata:\n  type: {type}\n  tags: [{tags}]\n---\n\n{body}\n"


def write(root: Path, rel: str, **kw):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(FM.format(**kw), encoding="utf-8")


class RedactionTests(unittest.TestCase):
    def check(self, text, label, must_vanish):
        out, counts = pack.redact(text)
        self.assertNotIn(must_vanish, out, out)
        self.assertIn(f"[REDACTED:{label}]", out, out)
        self.assertGreaterEqual(counts.get(label, 0), 1)
        return out

    def test_email(self):
        self.check("Write to alex.rivera+art@example.com today.", "email", "example.com")

    def test_phone_formats(self):
        for phone in ("+1 555 010 0199", "(555) 010-0199", "555-010-0199", "+61 400 000 000", "0400000000", "+15550100199"):
            with self.subTest(phone=phone):
                out, counts = pack.redact(f"Call me on {phone} after 5.")
                self.assertNotIn(phone, out, out)
                self.assertTrue(counts, out)

    def test_street_address(self):
        self.check("The studio is at 12 Harbour View Road, next to the bakery.", "address", "Harbour View Road")

    def test_account_numbers(self):
        self.check("Pay into account 12-3456-7890123 please.", "account", "3456")
        self.check("BSB 000-111 for the deposit", "account", "000-111")
        self.check("Card 4111 1111 1111 1111 expires soon", "number", "4111 1111")
        self.check("IBAN GB82 WEST 1234 5698 7654 32", "iban", "WEST 1234")

    def test_dates_times_and_plain_numbers_survive(self):
        text = "On 2026-03-14 at 21:00 I drew 3 pages; goal 50 users by 2026-12-31; 15% rate rise."
        out, counts = pack.redact(text)
        self.assertEqual(out, text)
        self.assertEqual(counts, {})

    def test_custom_rules_file(self):
        with tempfile.TemporaryDirectory() as d:
            rules = Path(d) / "rules.json"
            rules.write_text('{"surname": "(?i)\\\\bRivera\\\\b"}', encoding="utf-8")
            out, counts = pack.redact("Alex Rivera, email a@example.org", pack.compile_rules(str(rules)))
            self.assertEqual(out, "Alex [REDACTED:surname], email [REDACTED:email]")
            self.assertEqual(counts, {"surname": 1, "email": 1})


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write(self.root, "goals.md", name="Goals", desc="g", type="user", tags="goals", body="Ship the garden app.")
        write(self.root, "projects/app.md", name="App", desc="a", type="project", tags="garden, coding",
              body="Contact: alex@example.org")
        write(self.root, "sensitive/health/meds.md", name="Meds", desc="m", type="user", tags="garden",
              body="SECRET-HEALTH-DETAIL")
        (self.root / "notes.md").write_text(
            "---\nname: Flagged\ndescription: f\nmetadata:\n  type: note\n  tags: [garden]\n"
            "  sensitivity: sensitive\n---\nFLAGGED-DETAIL\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_sensitive_excluded_by_default(self):
        text, info = pack.build_pack(self.root, tags=["garden"])
        self.assertNotIn("SECRET-HEALTH-DETAIL", text)
        self.assertNotIn("FLAGGED-DETAIL", text)
        self.assertEqual(info["skipped_sensitive"], 2)
        self.assertEqual(info["files"], ["projects/app.md"])

    def test_sensitive_included_only_with_flag(self):
        text, info = pack.build_pack(self.root, tags=["garden"], include_sensitive=True)
        self.assertIn("SECRET-HEALTH-DETAIL", text)
        self.assertIn("FLAGGED-DETAIL", text)
        self.assertIn("INCLUDED", text)

    def test_redaction_applies_to_pack(self):
        text, info = pack.build_pack(self.root, folders=["projects"], do_redact=True)
        self.assertNotIn("alex@example.org", text)
        self.assertEqual(info["redactions"], {"email": 1})

    def test_topic_and_folders(self):
        text, info = pack.build_pack(self.root, topic="ship garden")
        self.assertEqual(info["files"], ["goals.md"])
        text, info = pack.build_pack(self.root, folders=["projects"])
        self.assertEqual(info["files"], ["projects/app.md"])

    def test_max_chars_drops_files(self):
        text, info = pack.build_pack(self.root, folders=["goals.md", "projects"], max_chars=150)
        self.assertEqual(len(info["files"]), 1)
        self.assertEqual(len(info["dropped"]), 1)

    def test_workspace_files(self):
        (self.root / "CLAUDE.md").write_text("@AGENTS.md\n")
        (self.root / "AGENTS.md").write_text("# Rules\n\nROOT-RULES\n")
        proj = self.root / "projects" / "garden"
        (proj / "notes").mkdir(parents=True)
        (proj / "STATUS.md").write_text("# Status\n\nHANDBACK-NOTE\n")
        tpl = self.root / "projects" / "_template"
        tpl.mkdir(parents=True)
        (tpl / "README.md").write_text("# Project name\n\nTEMPLATE-TEXT\n")
        text, info = pack.build_pack(self.root, folders=["projects", "AGENTS.md", "CLAUDE.md"])
        self.assertIn("HANDBACK-NOTE", text)
        self.assertIn("## projects/garden/STATUS.md", text)   # meta files are named by their folder
        self.assertIn("ROOT-RULES", text)
        self.assertNotIn("TEMPLATE-TEXT", text)                # copy-me templates are skipped
        self.assertNotIn("CLAUDE.md", " ".join(info["files"]))  # the pointer adds nothing

    def test_cli_requires_a_selection(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            pack.main([str(self.root)])


if __name__ == "__main__":
    unittest.main()

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import index  # noqa: E402
import lint  # noqa: E402
import podlib  # noqa: E402


def mem(name, desc, mtype, body="A fact.\n\n**Why:** x\n\n**How to apply:** y\n"):
    return f"---\nname: {name}\ndescription: {desc}\nmetadata:\n  type: {mtype}\n---\n\n{body}"


class FrontmatterTests(unittest.TestCase):
    def test_parse_nested_and_lists(self):
        meta = podlib.parse_yaml_subset(
            'name: "Quoted: name"\ndescription: hook\nmetadata:\n  type: user\n  tags: [a, b]\n'
            "aliases:\n  - one\n  - two\n")
        self.assertEqual(meta["name"], "Quoted: name")
        self.assertEqual(meta["metadata"], {"type": "user", "tags": ["a", "b"]})
        self.assertEqual(meta["aliases"], ["one", "two"])

    def test_no_frontmatter(self):
        fm, body = podlib.split_frontmatter("# Just a note\n")
        self.assertIsNone(fm)
        self.assertEqual(body, "# Just a note\n")


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "memory").mkdir()
        (self.root / "sensitive" / "health").mkdir(parents=True)
        (self.root / "about-me.md").write_text(mem("About me", "who I am", "user"), encoding="utf-8")
        (self.root / "memory" / "b-pref.md").write_text(mem("Short answers", "lead with the point", "feedback"))
        (self.root / "memory" / "a-me.md").write_text(mem("Night owl", "works late", "user", "See [[b-pref]]."))
        (self.root / "sensitive" / "health" / "bloodwork.md").write_text(mem("Bloodwork", "PRIVATE-DESC", "user"))
        (self.root / "INDEX.md").write_text("# My pod\n\nHand-written intro.\n\n<!-- index:start -->\nold\n<!-- index:end -->\n\nFooter.\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_regenerates_both_indexes(self):
        changed = index.regenerate(self.root)
        self.assertEqual(sorted(changed), ["INDEX.md", "memory/MEMORY.md"])
        idx = (self.root / "INDEX.md").read_text()
        self.assertIn("Hand-written intro.", idx)
        self.assertIn("Footer.", idx)
        self.assertNotIn("\nold\n", idx)
        self.assertIn("- [About me](about-me.md) — who I am", idx)
        self.assertIn("[Memory index](memory/MEMORY.md)", idx)
        mem_idx = (self.root / "memory" / "MEMORY.md").read_text()
        self.assertIn("- [Night owl](a-me.md) — works late", mem_idx)
        self.assertIn("- [Short answers](b-pref.md) — lead with the point", mem_idx)
        self.assertLess(mem_idx.index("## user"), mem_idx.index("## feedback"))

    def test_workspace_layout(self):
        (self.root / "AGENTS.md").write_text("# Rules\n")
        (self.root / "CLAUDE.md").write_text("@AGENTS.md\n")
        proj = self.root / "projects" / "garden"
        proj.mkdir(parents=True)
        (proj / "README.md").write_text(mem("Garden app", "swap cuttings", "project"))
        (proj / "AGENTS.md").write_text("# Brief\n")
        (proj / "STATUS.md").write_text("# Status\n")
        tpl = self.root / "projects" / "_template"
        (tpl / "notes").mkdir(parents=True)
        (tpl / "README.md").write_text(mem("Project name", "one line", "project"))
        (tpl / "notes" / "README.md").write_text("# notes\n")
        (self.root / "library").mkdir()
        (self.root / "library" / "README.md").write_text("# library/\n\nReusable things. More text here.\n")
        index.regenerate(self.root)
        idx = (self.root / "INDEX.md").read_text()
        self.assertIn("- [AGENTS.md](AGENTS.md) — rules every agent reads first", idx)
        self.assertIn("- [Garden app](projects/garden/README.md) — swap cuttings", idx)
        self.assertIn("- [projects/_template/](projects/_template/README.md) — copy this folder", idx)
        self.assertIn("- [library/](library/README.md) — Reusable things.", idx)
        for absent in ("CLAUDE.md", "STATUS.md", "garden/AGENTS.md", "_template/notes", "Project name"):
            self.assertNotIn(absent, idx)
        errors, warnings = lint.lint(self.root)  # workspace files need no frontmatter
        self.assertEqual((errors, warnings), ([], []))

    def test_sensitive_names_never_listed(self):
        index.regenerate(self.root)
        idx = (self.root / "INDEX.md").read_text()
        self.assertIn("`sensitive/health/`", idx)
        self.assertNotIn("bloodwork", idx.lower())
        self.assertNotIn("PRIVATE-DESC", idx)

    def test_check_mode_and_idempotence(self):
        self.assertTrue(index.regenerate(self.root, check=True))
        self.assertIn("\nold\n", (self.root / "INDEX.md").read_text())  # check mode writes nothing
        index.regenerate(self.root)
        self.assertEqual(index.regenerate(self.root, check=True), [])

    def test_lint_clean_after_index(self):
        index.regenerate(self.root)
        errors, warnings = lint.lint(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


class LintTests(unittest.TestCase):
    def test_finds_problems(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "memory").mkdir()
            (root / "memory" / "bad-type.md").write_text(mem("X", "y", "diary", "See [[missing-file]]."))
            (root / "memory" / "no-fm.md").write_text("just text\n")
            (root / "keys.md").write_text(mem("Keys", "oops", "note", "api_key = abcdef1234567890"))  # gitleaks:allow (fake value for the lint test)
            (root / "big.md").write_text(mem("Big", "b", "note", "x" * 9000))
            errors, warnings = lint.lint(root)
            joined = "\n".join(errors + warnings)
            self.assertIn("metadata.type 'diary'", joined)
            self.assertIn("broken link [[missing-file]]", joined)
            self.assertIn("memory/no-fm.md: no frontmatter", joined)
            self.assertIn("looks like a secret", joined)
            self.assertIn("big.md", joined)

    def test_shipped_template_has_workspace_layout(self):
        t = ROOT / "template"
        for rel in ("AGENTS.md", "CLAUDE.md", "INDEX.md", "personal/about-me.md", "memory/MEMORY.md",
                    "library/brand", "library/refs", "library/templates", "notes/research", "notes/briefs",
                    "notes/workflows", "study", "system", "sensitive/health", "sensitive/finance"):
            self.assertTrue((t / rel).exists(), rel)
        projects = [p for p in (t / "projects").iterdir() if p.is_dir()]
        self.assertGreaterEqual(len(projects), 3)  # _template + two examples
        for p in projects:
            for f in ("README.md", "AGENTS.md", "CLAUDE.md", "STATUS.md", "notes"):
                self.assertTrue((p / f).exists(), f"{p.name}/{f}")

    def test_shipped_template_is_clean(self):
        errors, warnings = lint.lint(ROOT / "template")
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(index.regenerate(ROOT / "template", check=True), [])


if __name__ == "__main__":
    unittest.main()

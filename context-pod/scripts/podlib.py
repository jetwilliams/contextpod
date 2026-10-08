"""Shared helpers for the context-pod scripts (Python 3 standard library only).

A pod file is a markdown file that may start with YAML frontmatter:

    ---
    name: Prefers short answers
    description: One-line hook shown in the index
    metadata:
      type: feedback
      tags: [communication, writing]
      sensitivity: private
      updated: 2026-01-15
    ---

Only a small, predictable subset of YAML is supported on purpose: `key: value`,
one level of nesting, inline lists `[a, b]` and block lists (`- item`).
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

MEMORY_TYPES = ("user", "feedback", "project", "reference")
# Types allowed outside memory/ as well (journal entries, plain notes).
POD_TYPES = MEMORY_TYPES + ("journal", "note")

# Files that describe the pod rather than hold context; they need no frontmatter.
# Workspace files (AGENTS.md, CLAUDE.md, STATUS.md) are free-form markdown too.
META_FILES = {"README.md", "INDEX.md", "MEMORY.md", "AGENTS.md", "CLAUDE.md", "STATUS.md"}

# Folders that hold copy-me templates (projects/_template/); skipped by packs.
TEMPLATE_DIR_PREFIX = "_template"

# Folders never walked: version control, build output, generated packs.
SKIP_DIRS = {".git", "packs", "__pycache__", "node_modules", ".obsidian"}

SENSITIVE_DIR = "sensitive"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+\.md)(?:#[^)]*)?\)")


@dataclass
class PodFile:
    path: Path          # absolute path
    rel: str            # path relative to the pod root, always with "/"
    meta: dict = field(default_factory=dict)
    body: str = ""
    has_frontmatter: bool = False
    frontmatter_error: str | None = None

    @property
    def name(self) -> str:
        if self.meta.get("name"):
            return str(self.meta["name"])
        p = Path(self.rel)
        if p.name in META_FILES and p.parent.as_posix() != ".":
            return f"{p.parent.as_posix()}/{p.name}"   # e.g. projects/plant-swap-app/STATUS.md
        return p.stem

    @property
    def description(self) -> str:
        return str(self.meta.get("description") or "")

    @property
    def mtype(self) -> str:
        md = self.meta.get("metadata")
        return str(md.get("type", "")) if isinstance(md, dict) else ""

    @property
    def tags(self) -> list[str]:
        md = self.meta.get("metadata")
        tags = md.get("tags", []) if isinstance(md, dict) else []
        if isinstance(tags, str):
            tags = [tags]
        return [str(t).lower() for t in tags]

    @property
    def sensitive(self) -> bool:
        return is_sensitive(self.rel, self.meta)


def _scalar(raw: str):
    s = raw.strip()
    if not s:
        return ""
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in inner.split(",")] if inner else []
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    return s


class FrontmatterError(ValueError):
    pass


def parse_yaml_subset(text: str) -> dict:
    """Parse the tiny YAML subset described in the module docstring."""
    root: dict = {}
    parent: dict | None = None      # dict for the current nested block
    list_target: tuple[dict, str] | None = None
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if stripped.startswith("- "):
            if list_target is None:
                raise FrontmatterError(f"line {lineno}: list item without a key")
            d, k = list_target
            if not isinstance(d.get(k), list):
                d[k] = []
            d[k].append(_scalar(stripped[2:]))
            continue
        if ":" not in stripped:
            raise FrontmatterError(f"line {lineno}: expected 'key: value'")
        key, _, value = stripped.partition(":")
        key = key.strip()
        if indent == 0:
            target = root
            parent = None
        else:
            if parent is None:
                raise FrontmatterError(f"line {lineno}: unexpected indentation")
            target = parent
        if value.strip() == "":
            if indent == 0:
                root[key] = {}
                parent = root[key]
                list_target = (root, key)
            else:
                target[key] = []
                list_target = (target, key)
        else:
            target[key] = _scalar(value)
            list_target = None
    # A key with neither children nor items: treat as empty string.
    for k, v in list(root.items()):
        if v == {}:
            root[k] = ""
    return root


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_text or None, body)."""
    if text.startswith("﻿"):
        text = text[1:]
    if not text.startswith("---"):
        return None, text
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:]).lstrip("\n")
    return None, text


def load(path: Path, root: Path) -> PodFile:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = split_frontmatter(text)
    pf = PodFile(path=path, rel=path.relative_to(root).as_posix(), body=body)
    if fm is not None:
        pf.has_frontmatter = True
        try:
            pf.meta = parse_yaml_subset(fm)
        except FrontmatterError as e:
            pf.frontmatter_error = str(e)
    return pf


def is_template(rel: str) -> bool:
    return any(part.startswith(TEMPLATE_DIR_PREFIX) for part in rel.split("/")[:-1])


def first_prose_line(body: str, limit: int = 140) -> str:
    """First sentence of the first real paragraph (skipping headings, code, quotes, tables).

    Used as the description for files without frontmatter, such as folder READMEs.
    """
    in_fence, para = False, []
    for line in body.splitlines() + [""]:
        s = line.strip()
        if s.startswith(("```", "~~~")):
            in_fence = not in_fence
            if para:
                break
            continue
        if in_fence:
            continue
        if not s or s.startswith(("#", ">", "|", "<!--", "- ", "* ", "1.")):
            if para:
                break
            continue
        para.append(s)
    text = " ".join(para)
    text = re.sub(r"^\*\*Summary:\*\*\s*", "", text).replace("**", "").replace("`", "")
    m = re.search(r"^(.+?[.!?:])(\s|$)", text)
    if m:
        text = m.group(1).rstrip(":")
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def is_sensitive(rel: str, meta: dict | None = None) -> bool:
    parts = rel.split("/")
    if SENSITIVE_DIR in parts[:-1]:
        return True
    md = (meta or {}).get("metadata")
    return isinstance(md, dict) and str(md.get("sensitivity", "")).lower() == "sensitive"


def iter_pod_files(root: Path, exts=(".md", ".txt")):
    """Yield every markdown/text file in the pod, sorted, skipping hidden and build dirs."""
    root = Path(root).resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if fn.startswith(".") or not fn.endswith(exts):
                continue
            yield load(Path(dirpath) / fn, root)


_FENCE_RE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.S | re.M)
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code, so examples inside them aren't treated as links."""
    return _INLINE_CODE_RE.sub("", _FENCE_RE.sub("", text))


def replace_between_markers(text: str, start: str, end: str, new_block: str) -> str:
    """Replace the text between two marker lines; append the block if markers are missing."""
    block = f"{start}\n{new_block.rstrip()}\n{end}"
    if start in text and end in text and text.index(start) < text.index(end):
        before = text[: text.index(start)]
        after = text[text.index(end) + len(end):]
        return before + block + after
    return text.rstrip() + "\n\n" + block + "\n"

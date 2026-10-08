#!/usr/bin/env python3
"""Regenerate INDEX.md and memory/MEMORY.md from each file's frontmatter.

Only the part between the marker comments is rewritten, so anything you
write above or below the markers stays.

    python3 scripts/index.py template           # rewrite both indexes
    python3 scripts/index.py template --check   # exit 1 if either is stale (for CI / pre-commit)

The sensitive layer is listed by folder only (no file names, no descriptions),
so INDEX.md is safe to include in a pack sent to a hosted model.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import podlib  # noqa: E402

INDEX_START, INDEX_END = "<!-- index:start -->", "<!-- index:end -->"
MEM_START, MEM_END = "<!-- memory:start -->", "<!-- memory:end -->"

INDEX_HEADER = """# Index

What lives in this pod, one line per file. Read this first, then open only what you need.
Regenerate with `python3 scripts/index.py <pod>`; edit outside the markers only.
"""

MEMORY_HEADER = """# Memory

One fact per file. One line per memory: `- [Title](file.md) — hook`.
Regenerate with `python3 scripts/index.py <pod>`; edit outside the markers only.
"""


def entry(pf: podlib.PodFile, link: str) -> str:
    line = f"- [{pf.name}]({link})"
    return line + (f" — {pf.description}" if pf.description else "")


def build_index_block(files: list[podlib.PodFile], has_memory: bool = False) -> str:
    groups: dict[str, list[tuple[str, int, str]]] = {}
    sensitive_dirs: set[str] = set()
    for pf in files:
        parts = pf.rel.split("/")
        if pf.sensitive:
            # Folder names only. Never leak sensitive file names or descriptions.
            if podlib.SENSITIVE_DIR in parts[:-1]:
                i = parts.index(podlib.SENSITIVE_DIR)
                depth = i + 2 if i + 2 < len(parts) else i + 1  # a folder, never a file name
                sensitive_dirs.add("/".join(parts[:depth]) + "/")
            else:
                sensitive_dirs.add("(files marked sensitivity: sensitive)")
            continue
        fname = parts[-1]
        folder = "/".join(parts[:-1])
        if len(parts) == 1:
            if fname == "AGENTS.md":
                groups.setdefault("Top level", []).append(
                    ("", 0, "- [AGENTS.md](AGENTS.md) — rules every agent reads first; start here"))
            if fname in podlib.META_FILES:
                continue  # INDEX.md, CLAUDE.md pointer, root README
        if parts[0] == "memory" and len(parts) == 2:
            continue  # memories (and MEMORY.md itself) are handled below
        if podlib.is_template(pf.rel):
            if fname == "README.md" and parts[-2].startswith(podlib.TEMPLATE_DIR_PREFIX):
                groups.setdefault(parts[0] + "/", []).append(
                    (folder, 0, f"- [{folder}/]({pf.rel}) — copy this folder to start a new one"))
            continue
        if fname in ("AGENTS.md", "CLAUDE.md", "STATUS.md"):
            continue  # listed in each project's README; the root AGENTS.md is above
        if fname == "README.md" and not pf.has_frontmatter:
            summary = podlib.first_prose_line(pf.body)
            line = f"- [{folder}/]({pf.rel})" + (f" — {summary}" if summary else "")
            rank = 0
        elif pf.has_frontmatter:
            line = entry(pf, pf.rel)
            rank = 0 if fname == "README.md" else 1
        else:
            continue
        group = parts[0] + "/" if len(parts) > 1 else "Top level"
        groups.setdefault(group, []).append((folder, rank, line))

    if has_memory:
        groups.setdefault("memory/", []).append(("memory", 0, "- [Memory index](memory/MEMORY.md) — one-fact memories, one line each"))
    out = []
    order = ["Top level"] + sorted(g for g in groups if g != "Top level")
    for g in order:
        if g in groups:
            out.append(f"## {g}\n")
            out.extend(line for _, _, line in sorted(groups[g], key=lambda t: (t[0], t[1], t[2].lower())))
            out.append("")
    if sensitive_dirs:
        out.append("## sensitive/ (SENSITIVE: encrypted at rest, never packed by default)\n")
        out.extend(f"- `{d}`" for d in sorted(sensitive_dirs))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def build_memory_block(files: list[podlib.PodFile]) -> str:
    mems = [pf for pf in files if pf.rel.startswith("memory/") and pf.rel.count("/") == 1
            and Path(pf.rel).name not in podlib.META_FILES]
    by_type: dict[str, list[podlib.PodFile]] = {}
    for pf in mems:
        by_type.setdefault(pf.mtype or "untyped", []).append(pf)
    out = []
    for t in list(podlib.MEMORY_TYPES) + sorted(k for k in by_type if k not in podlib.MEMORY_TYPES):
        if t not in by_type:
            continue
        out.append(f"## {t}\n")
        for pf in sorted(by_type[t], key=lambda p: p.name.lower()):
            if pf.sensitive:
                out.append(f"- [(sensitive memory)]({Path(pf.rel).name})")
            else:
                out.append(entry(pf, Path(pf.rel).name))
        out.append("")
    return "\n".join(out).rstrip() + "\n" if out else "_No memories yet._\n"


def render(path: Path, header: str, start: str, end: str, block: str) -> tuple[str, str]:
    old = path.read_text(encoding="utf-8") if path.exists() else header
    return old, podlib.replace_between_markers(old, start, end, block)


def regenerate(root: Path, check: bool = False) -> list[str]:
    """Rewrite the indexes. Returns the list of files that changed (or would change)."""
    root = Path(root).resolve()
    files = list(podlib.iter_pod_files(root))
    changed = []
    targets = [(root / "INDEX.md", INDEX_HEADER, INDEX_START, INDEX_END, build_index_block(files, (root / "memory").is_dir()))]
    if (root / "memory").is_dir():
        targets.append((root / "memory" / "MEMORY.md", MEMORY_HEADER, MEM_START, MEM_END, build_memory_block(files)))
    for path, header, start, end, block in targets:
        old, new = render(path, header, start, end, block)
        if old != new or not path.exists():
            changed.append(path.relative_to(root).as_posix())
            if not check:
                path.write_text(new, encoding="utf-8")
    return changed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pod", nargs="?", default=".", help="pod folder (default: current folder)")
    ap.add_argument("--check", action="store_true", help="don't write; exit 1 if an index is out of date")
    args = ap.parse_args(argv)
    changed = regenerate(Path(args.pod), check=args.check)
    if args.check:
        if changed:
            print("out of date: " + ", ".join(changed) + "  (run scripts/index.py)")
            return 1
        print("indexes up to date")
        return 0
    print("updated: " + ", ".join(changed) if changed else "indexes already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

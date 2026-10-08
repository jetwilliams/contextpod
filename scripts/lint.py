#!/usr/bin/env python3
"""Check a pod for problems before you rely on it (or share a pack from it).

Checks:
  - frontmatter: present, parseable, has name + description + metadata.type
  - memory/ files: type is one of user | feedback | project | reference
  - broken links: [[wiki-links]] (by file name without .md) and relative [text](file.md)
  - MEMORY.md lines that point at missing files, and memories missing from MEMORY.md
  - oversized files (default 8 KB: split them, one fact per file)
  - things that look like secrets (API keys, passwords) that should never be in a pod

    python3 scripts/lint.py template
    python3 scripts/lint.py ~/pod --max-kb 12 --strict   # warnings fail too

Exit code 1 if there are errors (or warnings with --strict).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import podlib  # noqa: E402

SECRET_RES = [
    re.compile(r"(?i)\b(api[_-]?key|secret|password|passwd|token|private[_-]?key)\b\s*[:=]\s*\S{8,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAGE-SECRET-KEY-1[0-9A-Z]{20,}\b"),
]
MAX_DESCRIPTION = 200


def lint(root: Path, max_kb: float = 8.0) -> tuple[list[str], list[str]]:
    root = Path(root).resolve()
    files = list(podlib.iter_pod_files(root))
    errors: list[str] = []
    warnings: list[str] = []
    stems = {Path(pf.rel).stem.lower() for pf in files}
    rels = {pf.rel for pf in files}

    for pf in files:
        fname = Path(pf.rel).name
        in_memory = pf.rel.startswith("memory/") and pf.rel.count("/") == 1
        is_meta = fname in podlib.META_FILES

        # --- frontmatter
        if not is_meta and not pf.rel.endswith(".txt"):
            if not pf.has_frontmatter:
                (errors if in_memory else warnings).append(f"{pf.rel}: no frontmatter")
            elif pf.frontmatter_error:
                errors.append(f"{pf.rel}: frontmatter does not parse ({pf.frontmatter_error})")
            else:
                for key in ("name", "description"):
                    if not pf.meta.get(key):
                        errors.append(f"{pf.rel}: frontmatter is missing '{key}'")
                if not isinstance(pf.meta.get("metadata"), dict):
                    errors.append(f"{pf.rel}: frontmatter is missing 'metadata:' (with 'type:')")
                elif not pf.mtype:
                    errors.append(f"{pf.rel}: frontmatter is missing 'metadata.type'")
                else:
                    allowed = podlib.MEMORY_TYPES if in_memory else podlib.POD_TYPES
                    if pf.mtype not in allowed:
                        errors.append(f"{pf.rel}: metadata.type '{pf.mtype}' is not one of {', '.join(allowed)}")
                if len(pf.description) > MAX_DESCRIPTION:
                    warnings.append(f"{pf.rel}: description is {len(pf.description)} chars; keep the hook short")

        # --- links (code spans and fenced blocks are examples, not links)
        prose = podlib.strip_code(pf.body)
        for m in podlib.WIKILINK_RE.finditer(prose):
            target = m.group(1).strip()
            if Path(target).stem.lower() not in stems:
                errors.append(f"{pf.rel}: broken link [[{target}]]")
        for m in podlib.MDLINK_RE.finditer(prose):
            target = m.group(1)
            if "://" in target:
                continue
            resolved = (pf.path.parent / target).resolve()
            try:
                rel = resolved.relative_to(root).as_posix()
            except ValueError:
                errors.append(f"{pf.rel}: link points outside the pod ({target})")
                continue
            if rel not in rels and not resolved.exists():
                errors.append(f"{pf.rel}: broken link ({target})")

        # --- size
        size_kb = pf.path.stat().st_size / 1024
        if size_kb > max_kb:
            warnings.append(f"{pf.rel}: {size_kb:.1f} KB (over {max_kb:g} KB; split it, one fact per file)")

        # --- secrets
        for lineno, line in enumerate(pf.path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if any(rx.search(line) for rx in SECRET_RES):
                errors.append(f"{pf.rel}:{lineno}: looks like a secret. Remove it; secrets never go in a pod")

    # --- memory index coverage
    mem_index = root / "memory" / "MEMORY.md"
    if mem_index.exists():
        text = podlib.strip_code(mem_index.read_text(encoding="utf-8"))
        linked = set(re.findall(r"\]\(([^)\s]+\.md)\)", text))
        for target in linked:
            if not (mem_index.parent / target).exists():
                errors.append(f"memory/MEMORY.md: points at missing file {target}")
        for pf in files:
            if pf.rel.startswith("memory/") and pf.rel.count("/") == 1 and Path(pf.rel).name not in podlib.META_FILES:
                if Path(pf.rel).name not in linked:
                    warnings.append(f"memory/MEMORY.md: {Path(pf.rel).name} is not listed (run scripts/index.py)")
    return errors, warnings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pod", nargs="?", default=".", help="pod folder (default: current folder)")
    ap.add_argument("--max-kb", type=float, default=8.0, help="warn above this file size (default 8)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)
    errors, warnings = lint(Path(args.pod), args.max_kb)
    for e in errors:
        print(f"ERROR   {e}")
    for w in warnings:
        print(f"warning {w}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

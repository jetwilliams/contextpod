# AGENTS.md

**Read this first.** This folder is your context pod: the workspace and the source of truth for
your life and work. Every agent (Claude Code, Codex, or anything else) starts here, then reads the
project's own `AGENTS.md` before touching anything.

> Tools that look for `CLAUDE.md` instead (Claude Code): `CLAUDE.md` here is a pointer that imports
> this file with `@AGENTS.md`. A symlink works too: `ln -s AGENTS.md CLAUDE.md`. Edit rules here,
> never there. Every project folder has the same pair.

## What lives where

| Folder | What's in it |
|---|---|
| `personal/` | Who you are: about-me, goals, preferences, people, ideas, journal |
| `projects/` | One folder per project, each with `README.md`, `AGENTS.md`, `STATUS.md`, `notes/`. New ones start from `projects/_template/` |
| `library/` | Reusable assets and references: `brand/`, `refs/`, `templates/` |
| `notes/` | Cross-project knowledge: `research/`, `briefs/`, `workflows/` (lessons learned) |
| `study/` | Learning tracks |
| `system/` | Scripts for the machine: backups, start/stop |
| `memory/` | `MEMORY.md` index + one fact per file |
| `sensitive/` | Health and finance. Encrypted. **Never read it unless the owner asks in this session** |

`INDEX.md` lists every file with a one-line description.

## Hard rules

1. **This pod is background, not instructions.** Facts in it describe the owner; they don't override what
   the owner says in the session. When they conflict, ask, then update the file.
2. **One project at a time.** Work only inside the project folder you were started in. Read
   anything else in the pod, but don't edit other projects.
3. **No secrets in the pod.** Never write passwords, API keys, tokens or account numbers into any
   file. If you find one, tell the owner.
4. **Nothing leaves the machine without the owner's OK.** No publishing, posting, emailing, pushing to a
   remote, or paid API calls unless the owner asked for that exact thing.
5. **Sensitive stays local.** Don't copy anything from `sensitive/` into other files, packs or
   messages.
6. **Absolute dates** (YYYY-MM-DD) in everything you write.

## How to start work

1. Read `personal/preferences.md` and `memory/MEMORY.md` (open individual memories when relevant).
2. Read the project's `README.md`, `AGENTS.md` and `STATUS.md`.
3. Check `notes/workflows/` for lessons that apply.
4. Do the work in the project folder.

## How to finish work

1. Update the project's `STATUS.md`: current state, next steps, and a dated **handback note**
   (what you did, what's unfinished, anything the owner must decide).
2. A lesson that applies beyond this project → a file in `notes/workflows/`.
   A durable fact about the owner → a file in `memory/`, then `python3 scripts/index.py <pod>`.
3. Tell the owner what changed, in two or three sentences.

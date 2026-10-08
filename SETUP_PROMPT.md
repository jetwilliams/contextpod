# One-prompt setup

Clone this repo, start your coding agent (Claude Code, Codex or similar) **inside the repo folder**,
and paste the prompt below. The agent checks what you already have, runs a short quiz about how
you live and work, then builds a pod shaped around you, not a generic one. Your answers are saved,
so you can run the same prompt again later to grow or reshape the pod.

```text
Build my context pod, using this repository as the guide.

STEP 0 — Read first.
Read README.md, docs/ (writing-good-context, plugging-in, privacy, workflow), the whole template/
folder and scripts/ (index.py, lint.py, pack.py).

STEP 1 — Check what already exists (read-only).
- Is there a pod.answers.md from a previous run? If yes, this is a RE-RUN: show me what's saved and
  ask what I want to change or add.
- Do I already have a pod or notes somewhere (a notes folder, an Obsidian vault, Notion/Google Docs
  exports, an existing AGENTS.md / CLAUDE.md / memory folder)? Ask me where, then list what's there
  WITHOUT changing anything.
- Python 3 version (the scripts need 3.9+); is git installed?

STEP 2 — The quiz. One short question at a time; skip anything already answered. Tell me I can say
"skip" to anything.
Where and how
- Where should the pod live (default ~/pod)? Do you want it in git (recommended, private repo only)?
- Which AI tools do you use (Claude Code, Codex, ChatGPT/Claude Projects, a local model)?
About you (keep it light, you can add more later)
- In a sentence or two: what do you do, and what are you into?
- What are you working towards this year?
- How do you like an assistant to talk to you (short/long, blunt/gentle, voice/text)?
Shape of your pod
- Which areas of life should it cover? (e.g. work, study, creative, health, money, family, travel)
  Only create folders for the ones you pick.
- What are your current projects (name + one line)? Any existing folders to adopt?
- Are you studying anything? (Each becomes a study track.)
- Do you keep a journal or want one?
Privacy
- Do you want a SENSITIVE layer (health, money)? If yes: encrypt it (age or git-crypt, see
  docs/privacy.md) and keep it local-only.
- Anything that must NEVER go into the pod?
- Which actions should agents always ask before doing (defaults: publishing, spending, emailing,
  pushing to a remote)?
Existing notes
- If I have existing notes: should we IMPORT copies of the useful parts, LINK to them, or leave them?
  (Never move or delete originals.)

STEP 3 — Plan.
Show me the folder tree you'll create (only the areas I chose) and what goes in each file. Wait for my OK.

STEP 4 — Build.
- Copy the template into the pod location, keep only the folders I chose, and fill the files from my
  answers (about-me, goals, preferences, AGENTS.md rules incl. my "always ask" list). Leave anything I
  skipped as a template prompt.
- Create one folder per project from projects/_template/, and study tracks if I'm studying.
- Seed memory/ with 2–4 one-fact memories from my answers (show them to me first).
- If I chose a sensitive layer: set up encryption, following docs/privacy.md, step by step.
  I type any passphrase MYSELF; never ask for it in chat.
- If importing notes: copy only what I approved into the right folders, converted to markdown.
- Run `python3 scripts/index.py <pod>` and `python3 scripts/lint.py <pod>` and fix any problems.
- If I chose git: `git init` the pod (private) and make a first commit. Don't add a remote unless I ask.
- Save my answers to pod.answers.md in the pod (no secrets, nothing sensitive).

STEP 5 — Show me how to use it.
In 5 short lines: start an agent in the pod or a project folder; how the agent reads AGENTS.md; how to
build a context pack for a chat app (scripts/pack.py); how to add a memory; how to re-run this setup.

Rules for you:
- Ask before creating, overwriting or importing anything. Never move or delete my originals.
- Nothing from the sensitive layer goes into packs, other files or chat.
- Never ask for passwords, passphrases or keys in chat.
```

## Re-running

Run the same prompt any time: a new area of life, new projects, a new AI tool, or a tidy-up. The agent
reads `pod.answers.md` and only changes what you ask for.

# Writing good context

A model reads your pod the way a new colleague reads a handover note: quickly, literally, and
without the background you carry in your head. These habits make the difference between a pod
that helps and a pile of text the model skims past.

## 1. One fact per file

Each memory file holds one thing: one preference, one decision, one deadline. Small files are easy
to update, easy to delete when they stop being true, and easy for a model (or a script) to pick
out without dragging in everything else.

Bad: `notes-about-me.md`, 4,000 words, updated in 2024.
Good: `feedback-no-bullet-walls.md`, 120 words, `updated: 2026-03-02`.

Bigger topics (a project, your goals) get one file each, but split them when they pass a few
screens. `scripts/lint.py` warns above 8 KB.

## 2. Summary first

Put the point in the first line or two: a `**Summary:**` line in long files, and a one-sentence
fact at the top of a memory. Models weight the start of a file heavily, and you'll skim it the
same way in a year.

The `description:` in the frontmatter is the hook shown in the index. Write it so a model can
decide from that line alone whether to open the file.

## 3. Say why, and how to apply it

A rule without a reason gets applied blindly, including where it doesn't fit. Memories use two
lines for this:

- **Why:** what happened or what you care about that makes this true.
- **How to apply:** what the model should actually do differently.

"Don't suggest early meetings" is a rule. "Focused hours are 21:00 to 01:00 because the house is
quiet then; start daily plans at 10:30" lets the model reason about a case you didn't foresee.

## 4. Absolute dates, always

"Last week", "recently" and "next month" are meaningless once the file is a month old, and the
model can't know when you wrote them. Write `2026-03-14`. Give deadlines a date, decisions the date
you made them, and every file an `updated:` field. When two files disagree, the newer one wins.

## 5. Leave things out

A pod is not an archive of everything. Leave out:

- **Secrets of any kind.** Passwords, API keys, recovery codes, account and card numbers, ID
  numbers. A model never needs them to help you. `scripts/lint.py` flags things that look like keys.
- **Other people's private details.** Use first names or roles; no contact details, no gossip, and
  nothing about someone else's health or money outside `sensitive/`.
- **Things that change daily** (to-do lists, inbox counts). They go stale before the next chat.
- **What the model already knows.** No need to explain what Python is; do explain that you're
  self-taught and learn from examples.
- **Instructions disguised as facts.** Your pod is background. Keep it descriptive ("I prefer short
  answers") rather than trying to reprogram the model.

## 6. Keep it current

Stale context is worse than none: the model will confidently act on what used to be true.

- When something changes, edit or delete the file the same day. Deleting is fine.
- Update the `updated:` date when you touch a file.
- Once a month, skim `INDEX.md` and `memory/MEMORY.md` and remove what's no longer true.
- When a journal entry contains a lasting fact ("I've stopped taking rush jobs"), copy that fact
  into a memory. The journal is the diary; `memory/` is the distilled version.
- Run `python3 scripts/index.py <pod>` after adding or renaming files, and `scripts/lint.py` before
  you build a pack.

## 7. Link related files

Use `[[file-name]]` (the file name without `.md`) to connect memories, and normal relative links
(`[goals](../goals.md)`) elsewhere. Links let a model follow a thread ("this deadline matters
because of that goal") without you repeating yourself. `scripts/lint.py` reports broken links.

## 8. Write in your own voice

Write how you'd explain it to a friend. Your phrasing is context too: it teaches the model your
tone, which matters when you ask it to draft something in your name.

## Checklist for a new file

- [ ] Frontmatter: `name`, `description`, `metadata.type`, `tags`, `updated`
- [ ] First line says the point
- [ ] Dates are absolute
- [ ] Why + how to apply (for memories)
- [ ] No secrets, no one else's contact details
- [ ] Linked to the files it relates to
- [ ] Sensitive? Then it goes in `sensitive/`, or gets `sensitivity: sensitive`

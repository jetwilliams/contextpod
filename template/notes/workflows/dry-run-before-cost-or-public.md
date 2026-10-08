---
name: Dry run before anything costs money or goes public
description: Lesson: rehearse every paid call, post or publish with a dry run, and get an explicit OK
metadata:
  type: feedback
  tags: [workflow, lessons, safety]
  updated: YYYY-MM-DD
---

# Dry run before anything costs money or goes public

> Example: replace with your own.

**Lesson:** before an agent runs anything that spends money (a paid API, a cloud job) or makes
something public (a post, a deploy, a push), it does a dry run first and shows what *would* happen.
The real run needs an explicit OK.

**Why:** both kinds of mistake are hard to undo. A loop calling a paid API can burn through a
budget in minutes, and a post can't be un-seen once it's out.

**How to apply:**

- Scripts that cost money or publish get a `--dry-run` flag, and it's the default.
- Dry-run output shows the count, the estimated cost, and exactly what would be posted.
- Set a hard spending cap per run.
- Every project's `AGENTS.md` says which actions need the owner's OK.

Applies to: every project. Related: [[feedback-free-local-first]]

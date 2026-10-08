---
name: Test on a copy first
description: Lesson from 2026-02: never let an agent experiment on the only working copy of anything
metadata:
  type: feedback
  tags: [workflow, lessons]
  updated: 2026-02-27
---

# Test on a copy first

**Lesson:** before an agent changes something that already works (the app's database, the
dashboard, a config file), make a copy and let it experiment there.

**Why:** on 2026-02-26 a "small cleanup" of the plant-swap database deleted twelve test listings
that took an evening to re-enter. Nothing important was lost, but it could have been.

**How to apply:** in every project's `AGENTS.md`, name the copy to experiment on (a `scratch/`
folder, a copy of the database). Agents ask before touching the real one.

Applies to: every project. Related: [[project-plant-swap-demo]]

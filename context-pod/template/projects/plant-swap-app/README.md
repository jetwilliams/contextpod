---
name: Plant-swap app
description: Small web app where neighbours list cuttings to swap; Alex's first real coding project
metadata:
  type: project
  tags: [coding, side-project, plant-swap]
  updated: 2026-03-14
---

# Plant-swap app

**Summary:** a tiny web app where people in one town list plant cuttings and arrange swaps. It's my first real software project, built to learn and to be used by the local garden club.

## Why

- Goal 2 for 2026: one small tool that real people use (see [goals](../../personal/goals.md)).
- The garden club swaps cuttings on a paper list that's always out of date.

## Decisions (don't reopen without a new reason)

- **2026-01-12: plain Python + SQLite, no framework-of-the-month.** Why: I want to understand every line. Revisit only past 500 users.
- **2026-02-03: no in-app messaging.** Why: moderation is work I can't do alone. Swaps are arranged by email outside the app.

## Open questions

- How to stop people listing things that aren't plants, without moderating by hand?
- Is a map view worth the effort for one town?

## Files

- `AGENTS.md`: brief and rules for the agent working here.
- `STATUS.md`: where it's at, next steps, last handback.
- `notes/`: design notes and decisions in progress.
- Code lives in `src/` (not part of the template).

Related: [[project-plant-swap-demo]], mentor sessions with Theo in [people](../../personal/people.md).

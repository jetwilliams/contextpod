# AGENTS.md: Jet-1 flight computer

> Example: replace with your own.

Read the pod's root `AGENTS.md` first; its hard rules apply here too. This file adds the project brief.

## Brief

Help design and build a model-rocket altimeter/logger: ESP32-class board, barometric sensor,
logs each flight and uploads it to a homelab dashboard after landing. Status: planning.

## Rules for this project

- Work only inside this folder.
- **Safety first.** Follow the model-rocketry safety code that applies where the owner flies.
  Version 1 must never control anything that fires or deploys. Flag anything about batteries,
  charging or mounting that could fail in flight.
- Keep a mass budget in grams in `notes/` and update it with every part change.
- Test on the bench before any flight: simulate pressure changes, check the log end to end.
- Local dashboard only; no cloud accounts.

## Start here

1. `STATUS.md` → the next step and the last handback.
2. `notes/` → open design notes.

## When you finish

Update `STATUS.md` (state, next steps, a dated handback note). Cross-project lessons go in
`../../notes/workflows/`.

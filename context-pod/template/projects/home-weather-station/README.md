---
name: Home weather station
description: A small sensor box on the balcony that logs temperature, humidity and pressure to a local dashboard
metadata:
  type: project
  tags: [hardware, electronics, weather]
  updated: 2026-03-08
---

# Home weather station

**Summary:** a microcontroller with a temperature/humidity/pressure sensor on the balcony, logging every five minutes to a dashboard on the home network. A weekend hardware project to learn soldering and basic electronics.

## Why

- Curiosity: the balcony gets much hotter than the forecast says, and I want the numbers.
- Practice for the "drawing for coders" workshop idea: something physical to show.

## Decisions

- **2026-02-28: local network only, no cloud service.** Why: no accounts, no subscriptions, data stays home.
- **2026-03-01: battery + small solar panel**, no cable through the window.

## Files

- `AGENTS.md`: brief and rules for the agent working here.
- `STATUS.md`: where it's at, next steps, last handback.
- `notes/`: wiring notes, parts list.

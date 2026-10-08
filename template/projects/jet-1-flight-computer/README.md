---
name: Jet-1 flight computer
description: A tiny model-rocket altimeter/logger that records each flight and uploads it to a homelab dashboard
metadata:
  type: project
  tags: [rocketry, electronics, homelab]
  updated: YYYY-MM-DD
---

# Jet-1 flight computer

> Example: replace with your own.

**Summary:** a small, light flight computer for model rockets: an ESP32-class board with a
barometric pressure sensor logs altitude through each flight, then uploads the log over Wi-Fi to a
homelab dashboard once it's back in range.

**Status:** planning.

## Why

- Real data from every flight: apogee, ascent rate, descent rate.
- Learn embedded programming with a project that has a hard size and weight limit.

## Planned parts

| Part | Job |
|---|---|
| ESP32-class microcontroller board (small form factor) | Logging, Wi-Fi upload |
| Barometric pressure sensor breakout | Altitude from air pressure |
| Small LiPo cell + charger | Power |
| On-board flash or microSD | Flight log storage |

## Decisions

- **Version 1 is a logger only.** No deployment charges or anything that fires; recovery stays
  with the rocket's standard motor ejection.
- **Upload after landing, not live telemetry.** Simpler, lighter, and needs no radio licence.

## Open questions

- Sample rate vs. storage: how fast to log during ascent?
- How to detect launch and apogee reliably from pressure alone?

## Files

- `AGENTS.md`: brief and rules for the agent working here.
- `STATUS.md`: where it's at, next steps, last handback.
- `notes/`: firmware design, mass budget, test plans.

Related: [[feedback-free-local-first]], [[user-document-builds]]

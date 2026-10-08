---
name: Flight computer firmware plan
description: States the firmware moves through, from power-on to upload
metadata:
  type: project
  tags: [rocketry, firmware]
  updated: YYYY-MM-DD
---

# Firmware plan

> Example: replace with your own.

**Summary:** a simple state machine, logging at a low rate on the pad and a high rate in flight.

1. **Idle on the pad:** log slowly, keep a rolling buffer so the launch itself is captured.
2. **Launch detected** (altitude rising fast): switch to the high logging rate.
3. **Apogee** (altitude stops rising): mark it in the log.
4. **Descent → landed** (altitude steady): stop high-rate logging, save the file.
5. **Upload:** join the home Wi-Fi when in range and send the log to the dashboard.

Open: thresholds for each transition, and how to filter sensor noise.

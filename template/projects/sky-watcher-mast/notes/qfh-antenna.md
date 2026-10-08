---
name: QFH antenna notes
description: Why a QFH for weather satellites, and the open questions before building one
metadata:
  type: reference
  tags: [radio, antenna, sdr]
  updated: YYYY-MM-DD
---

# QFH antenna notes

> Example: replace with your own.

**Summary:** a quadrifilar helix (QFH) antenna suits polar-orbiting weather satellites because it
receives circularly polarised signals from horizon to overhead without being pointed.

- Target band: around 137 MHz.
- Check which weather satellites are still transmitting before building; the active list changes.
- Element lengths come from an online QFH calculator; record the inputs (frequency, conductor
  diameter, ratio) here so the build can be repeated.
- Materials to compare: copper pipe vs coax for the elements; PVC pipe for the frame.

## Open questions

- Pre-amplifier (LNA) at the antenna, or not?
- Which software to decode and schedule passes?

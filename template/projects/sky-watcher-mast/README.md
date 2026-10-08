---
name: Sky-watcher mast
description: A light rooftop/portable radio mast that tracks aircraft (ADS-B), receives weather satellites and relays a Meshtastic mesh
metadata:
  type: project
  tags: [radio, sdr, hardware, homelab]
  updated: YYYY-MM-DD
---

# Sky-watcher mast

> Example: replace with your own.

**Summary:** a lightweight mast that can sit on a roof or go out portable. It holds a small
computer and a software-defined radio (SDR) that track aircraft over ADS-B, a homemade QFH antenna
for weather-satellite images, and a solar-powered Meshtastic relay node, all in a 3D-printed
weatherproof box.

**Status:** planning.

## Why

- Learn radio by building: antennas, SDR, decoding real signals.
- See what's overhead (aircraft, satellites) on a home dashboard instead of someone else's app.
- Add a node to the local Meshtastic mesh, so off-grid messages travel further.

## Planned parts

| Part | Job |
|---|---|
| Raspberry Pi Zero 2 W | Runs the decoders, serves data to the homelab |
| USB SDR dongle + 1090 MHz antenna | ADS-B aircraft tracking |
| Homemade QFH antenna (137 MHz) | Weather-satellite reception |
| LoRa board running Meshtastic + small solar panel | Mesh relay, independent of the Pi |
| 3D-printed enclosure (UV-resistant filament) | Weatherproof box with cable glands and a vent |

## Decisions

- **Receive-only radio for the SDR side.** No transmitting except the Meshtastic node, which
  runs in the licence-free LoRa band for the region.
- **The mesh relay is a separate, self-powered board**, so it keeps working if the Pi is down.

## Open questions

- One SDR can't listen on 1090 MHz and 137 MHz at once: schedule satellite passes, or add a
  second dongle (the Pi Zero has a single USB port, so that means a powered hub)?
- How light can the mast be and still survive wind?

## Files

- `AGENTS.md`: brief and rules for the agent working here.
- `STATUS.md`: where it's at, next steps, last handback.
- `notes/`: design notes, antenna maths, wiring.

Related: [[feedback-free-local-first]], [[user-document-builds]]

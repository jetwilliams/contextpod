# Status: home weather station

**Updated:** 2026-03-08

## Current state

- Sensor reads correctly on the breadboard; values print to the serial console.
- Solar charging not wired yet.

## Next steps

1. Solder the sensor onto a perfboard (weekend of 2026-03-21).
2. Write the logger: one reading every 5 minutes to a CSV file.
3. Simple dashboard page with the last 24 hours.

## Handback notes (newest first)

### 2026-03-08, agent session

- Did: firmware reads the sensor and prints readings once a second.
- Unfinished: deep-sleep between readings (battery life).
- Needs Alex: confirm the battery's capacity from the label before we size the solar panel.

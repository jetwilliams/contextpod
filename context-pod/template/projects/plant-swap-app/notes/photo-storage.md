---
name: Photo storage options
description: Where plant photos should live; two options with trade-offs, decision pending
metadata:
  type: project
  tags: [plant-swap, design]
  updated: 2026-03-14
---

# Photo storage options

**Summary:** decide by 2026-03-19. Leaning towards A.

- **A. Files on disk, path in SQLite.** Simple, easy to back up with the rest of the app. Needs a cleanup job for deleted listings.
- **B. Images inside SQLite as blobs.** One file to back up, but the database grows fast and gets slow to copy.

Decision: _pending (Alex)_.

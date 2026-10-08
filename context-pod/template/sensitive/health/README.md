# health/ (SENSITIVE: example structure only)

Suggested files (one topic per file, each with frontmatter and `sensitivity: sensitive`):

```
health/
  overview.md          # one-paragraph summary: conditions, allergies, what matters most
  medications.md       # name, dose, since when, prescribed for, side effects noticed
  appointments.md      # dated list: YYYY-MM-DD, who (role, not full name), outcome, follow-up
  habits.md            # habits you're building or breaking, with start dates and honest notes
  mental-health.md     # what helps, what doesn't, warning signs, who to call
```

Example frontmatter:

```yaml
---
name: Medications
description: Current medications and doses, updated after each appointment
metadata:
  type: user
  tags: [health]
  sensitivity: sensitive
  updated: 2026-01-01
---
```

Example line (fictional): `- 2026-01-10 · GP · annual check-up · all normal · next one 2027-01`

Leave out: insurance or patient ID numbers, full names and addresses of clinics or doctors,
anything you'd only need for paperwork. Those live in your password manager or filing cabinet.

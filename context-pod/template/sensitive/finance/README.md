# finance/ (SENSITIVE: example structure only)

Suggested files (one topic per file, each with frontmatter and `sensitivity: sensitive`):

```
finance/
  overview.md          # one paragraph: income sources, monthly costs, the one money worry
  budget.md            # categories and monthly targets, rounded numbers
  income.md            # clients or employers by role, typical monthly amount, payment habits
  goals.md             # savings or debt goals, each with a target amount and a date
  decisions.md         # dated money decisions and why (so an assistant doesn't reopen them)
```

Example frontmatter:

```yaml
---
name: Money goals
description: Savings and debt goals for 2026, each with an amount and a date
metadata:
  type: user
  tags: [finance, goals]
  sensitivity: sensitive
  updated: 2026-01-01
---
```

Example line (fictional): `- Emergency fund: 3 months of costs by 2026-12-31 (currently about 1 month)`

**Never write here:** account or card numbers, logins, passwords, PINs, tax file or social
security numbers, or recovery codes. A model never needs them to give you money advice.
Rounded numbers are enough.

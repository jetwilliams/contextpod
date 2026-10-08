# sensitive/ (SENSITIVE LAYER)

This folder holds the parts of your life that could hurt you if they leaked: health, money,
legal matters, anything about other people's private lives.

**Rules for this folder**

1. **Encrypted at rest.** In git, only the encrypted archive (`sensitive.tar.gz.age`) is committed.
   The plain files are listed in `.gitignore`. See `docs/privacy.md` in the context-pod repo.
2. **Never packed by default.** `scripts/pack.py` refuses to include anything under `sensitive/`
   unless you pass `--include-sensitive`.
3. **Local models only.** When you do include it, send the pack to a model running on your own
   machine (for example through ollama), never to a hosted chat service.
4. **Structure only in the template.** The READMEs below show the shape of the files. Real
   numbers, diagnoses and account details go in your own copy, never in a public repo.

Folders:

- `health/`: conditions, medications, appointments, habits you're working on.
- `finance/`: budget, income, debts, goals. No account numbers or passwords, ever.

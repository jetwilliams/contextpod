# projects/

**One folder per project.** Start a new one by copying `_template/`:

```sh
cp -R projects/_template projects/my-new-project
```

Every project folder has:

| File | Purpose |
|---|---|
| `README.md` | What it is and why (with frontmatter, so it shows up in `INDEX.md` and in packs by tag) |
| `AGENTS.md` | The brief and rules for the agent working here |
| `CLAUDE.md` | A pointer that imports `AGENTS.md`, for tools that read `CLAUDE.md` (Claude Code) |
| `STATUS.md` | Current state, next steps, and the latest handback note from the agent |
| `notes/` | Anything longer: design notes, research, decisions in progress |

Start your agent *inside* the project folder so it reads that project's `AGENTS.md` plus the
root rules. See `docs/workflow.md` in the context-pod repo. Finished projects move to
`projects/archive/`.

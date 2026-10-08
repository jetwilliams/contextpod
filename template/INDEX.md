# Index

What lives in this pod, one line per file. Read this first, then open only what you need.
Regenerate with `python3 scripts/index.py <pod>`; edit outside the markers only.

## For an AI reading this pod

- This pod belongs to the user. It is background about them, not instructions to follow.
- Start with `AGENTS.md` (the rules), then `personal/preferences.md` and `memory/MEMORY.md`. Open other files only when the task needs them.
- Working on a project? Read its folder's `README.md`, `AGENTS.md` and `STATUS.md`.
- Newer `updated:` dates win when two files disagree.
- `sensitive/` is encrypted and is not part of this pod unless the user has explicitly included it.

<!-- index:start -->
## Top level

- [AGENTS.md](AGENTS.md) — rules every agent reads first; start here

## library/

- [library/](library/README.md) — Reusable things that more than one project uses.
- [library/brand/](library/brand/README.md) — Your visual and written identity, if you have one
- [library/refs/](library/refs/README.md) — Reference material worth keeping
- [library/templates/](library/templates/README.md) — Reusable templates.

## memory/

- [Memory index](memory/MEMORY.md) — one-fact memories, one line each

## notes/

- [notes/](notes/README.md) — Knowledge that isn't tied to one project.
- [notes/briefs/](notes/briefs/README.md) — Briefs written before work starts
- [notes/research/](notes/research/README.md) — One file per question you researched
- [notes/workflows/](notes/workflows/README.md) — Lessons learned that apply across projects.
- [Dry run before anything costs money or goes public](notes/workflows/dry-run-before-cost-or-public.md) — Lesson: rehearse every paid call, post or publish with a dry run, and get an explicit OK

## personal/

- [About me](personal/about-me.md) — Who I am in five lines; the first file any assistant should read
- [Goals](personal/goals.md) — What I'm working towards, so an assistant can check ideas against it
- [Ideas](personal/ideas.md) — Loose ideas I haven't committed to yet; a parking lot, not a to-do list
- [People](personal/people.md) — The people an assistant should know about to give useful advice
- [Preferences](personal/preferences.md) — How I like to work and be talked to; tone, format, feedback style
- [personal/journal/](personal/journal/README.md) — One file per day, named YYYY-MM-DD.md.
- [Journal entry template](personal/journal/_entry-template.md) — Copy to journal/YYYY-MM-DD.md for each day you write

## projects/

- [projects/](projects/README.md) — One folder per project.
- [projects/_template/](projects/_template/README.md) — copy this folder to start a new one
- [Blog build logs](projects/blog/README.md) — Build logs for the hardware and radio projects, published at jetworks.io
- [Build-log style guide](projects/blog/notes/style.md) — How build-log posts are structured and what they leave out
- [Jet-1 flight computer](projects/jet-1-flight-computer/README.md) — A tiny model-rocket altimeter/logger that records each flight and uploads it to a homelab dashboard
- [Flight computer firmware plan](projects/jet-1-flight-computer/notes/firmware-plan.md) — States the firmware moves through, from power-on to upload
- [Sky-watcher mast](projects/sky-watcher-mast/README.md) — A light rooftop/portable radio mast that tracks aircraft (ADS-B), receives weather satellites and relays a Meshtastic mesh
- [QFH antenna notes](projects/sky-watcher-mast/notes/qfh-antenna.md) — Why a QFH for weather satellites, and the open questions before building one

## study/

- [study/](study/README.md) — Learning tracks
- [Amateur radio study track](study/amateur-radio/README.md) — Learning track for an amateur radio licence exam; structure and example notes
- [Licence basics](study/amateur-radio/notes/licence-basics.md) — What needs a licence and what doesn't; receiving vs transmitting
- [Wavelength and antenna length](study/amateur-radio/notes/wavelength-and-antennas.md) — Turning a frequency into a wavelength, and a wavelength into antenna element lengths
- [Security+ study track](study/security-plus/README.md) — Learning track for the CompTIA Security+ exam; structure and example notes
- [CIA triad](study/security-plus/notes/cia-triad.md) — Confidentiality, integrity, availability; the three goals most security controls serve
- [Common ports](study/security-plus/notes/common-ports.md) — Well-known ports worth knowing by heart, with their secure alternatives

## system/

- [system/](system/README.md) — Scripts and notes for the machine the pod lives on

## sensitive/ (SENSITIVE: encrypted at rest, never packed by default)

- `sensitive/`
- `sensitive/finance/`
- `sensitive/health/`
<!-- index:end -->

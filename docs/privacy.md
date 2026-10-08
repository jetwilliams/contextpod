# Privacy

A context pod is useful because it's personal, and that's exactly what makes it risky. The more
of your life it holds, the more it's worth to someone else. This page is the practical answer:
sort the pod into layers, encrypt the layer that could hurt you, decide which models may see
which layer, and back it all up without making a second copy that leaks.

## Three layers

| Layer | What goes in it | Who may read it |
|---|---|---|
| **Public** | Things you'd put on a personal website: working preferences, public projects, interests | Any model, any tool |
| **Private** (the default) | About me, goals, people, ideas, journal, most memories | Models you trust, ideally as a focused, redacted pack |
| **Sensitive** | Health, finance, legal, anything about someone else's private life | **Only a model running on your own machine.** Encrypted at rest |

How a file gets its layer:

- Anything under a `sensitive/` folder is sensitive, always. `scripts/pack.py` will not include it
  unless you pass `--include-sensitive`, and `scripts/index.py` lists only its folder names.
- Any other file can be marked in its frontmatter: `metadata.sensitivity: sensitive` gets the same
  treatment. `public` and `private` are labels for you; the scripts treat both as packable.
- When in doubt, it's private. When it's about your body, your money or another person's secrets,
  it's sensitive.

## Encrypt the sensitive layer

The plain-text files in `sensitive/` should exist on disk only while you're using them. Two good
options; pick one.

### Option 1: age (simplest)

[age](https://github.com/FiloSottile/age) is a small, modern file-encryption tool. Install it from
your package manager (`brew install age`, `apt install age`, `winget install FiloSottile.age`).

```sh
# Once: make a key. Store it OUTSIDE the pod and back it up offline (see Backups).
mkdir -p ~/.config/context-pod
age-keygen -o ~/.config/context-pod/pod.key      # prints your public key: age1...

# Lock: pack sensitive/ into one encrypted file, then remove the plain copy
tar -czf - -C ~/context-pod sensitive \
  | age -r age1yourpublickey... -o ~/context-pod/sensitive.tar.gz.age
find ~/context-pod/sensitive -name '*.md' ! -name README.md -delete   # READMEs hold no data

# Unlock for a session
age -d -i ~/.config/context-pod/pod.key ~/context-pod/sensitive.tar.gz.age \
  | tar -xzf - -C ~/context-pod
```

Prefer a passphrase to a key file? Use `age -p` to encrypt and `age -d` to decrypt; you'll be
prompted. Pick a long passphrase and keep it in your password manager.

The template's `.gitignore` already ignores everything under `sensitive/` except the READMEs, so
only `sensitive.tar.gz.age` ends up in git.

### Option 2: git-crypt (transparent, for git users)

[git-crypt](https://github.com/AGWA/git-crypt) encrypts chosen paths when you commit and decrypts
them when you check out, so you work with plain files and the remote only ever sees ciphertext.

```sh
cd ~/context-pod
git init && git-crypt init
printf 'sensitive/** filter=git-crypt diff=git-crypt\n' > .gitattributes
git-crypt export-key ~/.config/context-pod/git-crypt.key   # back this up offline
```

With git-crypt, delete the `sensitive/**` lines from the pod's `.gitignore` (git-crypt needs the
files tracked). Check it works before you push: `git-crypt status` should list your sensitive
files as encrypted. Things to know: file names and sizes are not encrypted, and once a file has
been pushed you can't take it back by rotating the key.

### Whichever you choose

- **Turn on full-disk encryption** (FileVault, BitLocker, LUKS). It protects everything, including
  the moments when `sensitive/` is unlocked.
- **The key never lives in the pod**, never goes in git, never goes in a pack. The pod's
  `.gitignore` blocks `*.key` and `.env` as a backstop.
- **Lock again when you're done.** An unlocked `sensitive/` folder is a plain-text folder.

## Health and finance go to local models only

Sending a document to a hosted model means it's stored on someone else's servers, under their
retention, training, staff-access and legal-request policies, which you don't control and which
can change. For most of the pod that's an acceptable trade. For your medical history and your
money it isn't.

- Run a local model with [ollama](https://ollama.com) or a similar runner, and only build
  `--include-sensitive` packs for it. See [plugging-in.md](plugging-in.md).
- Delete packs built with `--include-sensitive` after use (`packs/` is git-ignored, but it's still
  plain text on disk).
- Need a hosted model's help with a money or health question? Ask it in general terms ("how do
  people usually structure an emergency fund?") and apply the answer locally, rather than sending
  your numbers.

## Redaction is a safety net

`scripts/pack.py --redact` replaces emails, phone numbers, street addresses, P.O. boxes, IBANs,
long card-like numbers and labelled account numbers with `[REDACTED:...]`. Add your own patterns
(your surname, your street, your employer) in a JSON file and pass `--rules my-rules.json`:

```json
{ "surname": "(?i)\\bYourSurname\\b", "street": "(?i)your street name" }
```

Regexes can't catch everything: names, a unique job title, or a story only you could have told can
identify you just as well. **Always read a pack before you send it.**

## Never commit secrets

- Secrets don't belong in a pod at all: no passwords, API keys, recovery codes, PINs, card or
  account numbers, ID numbers. A model never needs them. Your password manager does.
- `scripts/lint.py` flags lines that look like keys or passwords. Run it before every commit, for
  example as a git pre-commit hook (`.git/hooks/pre-commit`, made executable):

  ```sh
  #!/bin/sh
  python3 /path/to/context-pod/scripts/lint.py . || exit 1
  python3 /path/to/context-pod/scripts/index.py . --check || exit 1
  ```

- If a secret does get committed: **change the secret first** (assume it's leaked), then remove it
  from history with `git filter-repo`. Deleting it in a new commit is not enough.
- Keep the git remote private, and turn on two-factor authentication for that account.

## Backups

A pod you lose is as bad as a pod that leaks. Use the 3-2-1 idea: three copies, on two kinds of
storage, one of them somewhere else.

1. **Your working copy** on your computer, with full-disk encryption.
2. **An encrypted remote.** A private git repository with the sensitive layer encrypted (age or
   git-crypt), or a backup tool that encrypts everything before upload, such as
   [restic](https://restic.net) to cloud storage.
3. **An offline drive.** An encrypted external drive you update every month or so and keep
   unplugged, ideally at a different address. It's your copy when an account gets locked or
   ransomware hits.

Two rules make this work:

- **Back up the key separately from the data**, for example printed on paper in a safe place, or in
  your password manager. A backup encrypted with a lost key is gone.
- **Test a restore** a few times a year: decrypt the remote copy on another machine and open a file.

## The threat model, in plain words

What this setup protects against:

- **A lost or stolen laptop.** Full-disk encryption, plus the sensitive layer locked with age.
- **A leaked or hacked git or cloud account.** The remote only holds the sensitive layer as
  ciphertext; without your key it's noise.
- **AI providers keeping, training on, or being made to hand over your data.** The sensitive layer
  never reaches them; the private layer goes as focused, redacted packs, not the whole pod.
- **Your own mistakes**, like pasting the wrong file. Packs exclude the sensitive layer by default
  and say in their header exactly what's inside.
- **Losing everything.** Three copies, one offline, plus a tested restore.

What it does not protect against:

- **Malware on your computer** while the sensitive layer is unlocked. Keep the machine updated and
  unlock only when needed.
- **Anything you've already sent** to a hosted model. It can't be recalled; decide before you send.
- **Someone who can force you** to unlock it. That's a legal and personal question, not a technical
  one.
- **Inference.** Even redacted, enough detail about your life identifies you. The fix is sending
  less, not redacting harder.

The short version: write it down, keep it on your own disk, encrypt what could hurt you, show
hosted models only what the task needs, and keep the most private layer on your own machine.

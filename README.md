# vem-project

[![Tests](https://github.com/ccp-volume-em/vem-project/actions/workflows/tests.yml/badge.svg)](https://github.com/ccp-volume-em/vem-project/actions/workflows/tests.yml)

One-line description of what this tool does for volume EM / CLEM data.

---

## About this template

*Delete this section once your project is set up.*

This is a [CCP-volumeEM](https://ccp-volume-em.github.io/guide/) starting point
for writing analysis code for volume electron microscopy (vEM) and correlative
light and electron microscopy (CLEM). It builds in the
[CCP-volumeEM good practice guide](https://ccp-volume-em.github.io/guide/) and
a simple, safe way of working:

- **Every change goes through a pull request** that's reviewed before it
  reaches `main`: by a colleague where possible, or by yourself with a
  [self-review checklist](REVIEWING.md#reviewing-your-own-pr) if you work alone.
- **Small, regular commits** with clear [Conventional Commit](https://www.conventionalcommits.org/)
  messages.
- **[Semantic Versioning](https://semver.org/)**, a [changelog](CHANGELOG.md),
  and tagged releases you can cite.
- **Tests that run automatically** on every pull request.
- **Large-data habits** from the start: lazy loading, OME-Zarr, physical units
  and provenance.

You can write code by hand or with any AI assistant. The rules for AI
assistants are in [AGENTS.md](AGENTS.md), which most tools read automatically.

### Start a new project

**New to coding or GitHub? Read [START_HERE.md](START_HERE.md) first.** It
explains everything in plain language, including these steps.

1. On GitHub, click **Use this template → Create a new repository**.
2. Clone your new repository and set up a Python environment (see
   [Installation](#installation)).
3. Ask your AI assistant to **run the `start-project` skill** (or to "follow
   `.agents/skills/start-project/SKILL.md`"). It asks a few questions and
   renames the example package, fills in authors and the licence, and opens a
   pull request. You can also follow that file by hand.
4. Read [CONTRIBUTING.md](CONTRIBUTING.md) for how day-to-day work flows.

### What's in the box

```text
├── START_HERE.md          plain-language guide for people new to coding or GitHub
├── AGENTS.md              instructions for any AI assistant (CLAUDE.md points here)
├── CONTRIBUTING.md        how to work: branches, commits, PRs, releases
├── REVIEWING.md           how to review a PR, someone else's or your own
├── CHANGELOG.md           what changed in each release
├── ROADMAP.md             what's planned next
├── CITATION.cff           how to cite this software
├── guidance/              the CCP-volumeEM guide, distilled into checklists
├── .agents/skills/        step-by-step procedures for AI assistants
│   ├── start-project/       set up a new repository from this template
│   ├── new-fiji-script/     write a Fiji script with a dialog, and its tests
│   ├── review-changes/      check a branch before opening a PR
│   ├── prepare-release/     choose a version and release
│   ├── update-guidance/     pull in changes to the CCP-volumeEM guide
│   └── update-from-template/ pull in later improvements to this template
├── src/vem_project/       example package: OME-Zarr I/O, a measurement, a CLI
├── fiji/                  example Fiji script (Groovy, with Script Parameters)
├── tests/                 tests of the code (Python and Fiji)
│   └── repository/          the template's checks on the repository itself
├── examples/              how to run it, and test data for Python and Fiji
├── docs/                  documentation site (optional) and the decision log
├── Dockerfile             container image
├── tools/                 repository maintenance scripts (not analysis)
└── .github/               CI workflows, issue and PR templates, Dependabot
```

The example package measures the physical volume of labelled objects in a
segmented OME-Zarr volume. It's deliberately small, but shows the patterns the
guide recommends. Keep it, adapt it, or delete it.

### AI assistants

| Assistant                                     | Reads `AGENTS.md`        | Skills                                               |
| --------------------------------------------- | ------------------------ | ---------------------------------------------------- |
| Claude Code                                   | yes, via `CLAUDE.md`     | yes, via the `.claude/skills` link                    |
| Codex, GitHub Copilot, Cursor, Gemini CLI, …  | yes, natively or by setting | from `.agents/skills/`, or ask it to read a skill file |
| Chat assistants (no repository access)        | paste it in              | paste the skill file in                               |

On Windows, git may check out `.claude/skills` as a small text file rather than
a link. Everything still works: ask the assistant to read the skill from
`.agents/skills/`.

### Keeping the guidance current

The CCP-volumeEM guide evolves. A scheduled GitHub Action checks it monthly
and opens an issue when it changes. Then ask your AI assistant to run the
**`update-guidance`** skill, which reads what changed, updates `guidance/` and
`AGENTS.md`, and opens a pull request for review. Check by hand with
`python tools/check_guidance.py`.

### Template versions

The template itself is versioned with git tags (`vX.Y.Z`) and GitHub
Releases, following [Semantic Versioning](https://semver.org/). Its
`CHANGELOG.md` describes each release. The version in `pyproject.toml` stays
at `0.0.0`, because every new project copies it and starts out unreleased;
tags aren't copied. To release the template, ask your AI assistant to run the
**`prepare-release`** skill, which knows the difference.

### Keeping a project up to date with the template

A project made from the template doesn't receive its later improvements by
itself. `.github/template.json` records which template version a project
came from. Ask your AI assistant to run the **`update-from-template`** skill:
it shows what has changed in the template since, merges the template's
changes into the shared files (rules, skills, checks, guidance) while keeping
the project's own edits, and opens a pull request for review. Check by hand
with `python tools/check_template.py`.

---

## Installation

<!-- The text between the --8<-- markers also appears on the documentation
site (docs/getting-started.md), so it's written only once. Keep links out of
it: they would break on the site. -->
<!-- --8<-- [start:install] -->
You need Python 3.11 or newer. Use a virtual environment, so this project's
packages don't interfere with others:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install "vem-project @ git+https://github.com/ccp-volume-em/vem-project"
```

Check it worked:

```bash
vem-project --version
```
<!-- --8<-- [end:install] -->

To work on the code itself, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Quick start

<!-- --8<-- [start:quickstart] -->
From a copy of the repository, make a small synthetic label volume and measure
the objects in it:

```bash
python examples/make_example_data.py
vem-project measure examples/params.yml
```

The first command writes `data/example_labels.ome.zarr`: two box-shaped
objects with 8 × 8 × 16 nm voxels. The second measures them and writes:

- `results/example/object_volumes.csv`: the volume of each object in nm³;
- `results/example/provenance.json`: the software version, parameters and
  inputs that produced it.

Object 1 is 8 × 20 × 20 voxels of 1,024 nm³ each, so its volume should be
3,276,800 nm³.
<!-- --8<-- [end:quickstart] -->

## Getting help

Report bugs and ask for features in the
[issue tracker](https://github.com/ccp-volume-em/vem-project/issues). For
general questions, use the [image.sc forum](https://forum.image.sc/).

## Contributing

Contributions are welcome. New to coding or GitHub? Start with
[START_HERE.md](START_HERE.md). The full details are in
[CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

If you use this software, please cite it using [CITATION.cff](CITATION.cff)
(GitHub's **Cite this repository** button).

## Use of AI

<!-- Describe substantive use of generative AI in developing this software,
or delete this section if none. See guidance/ai-use.md. -->

Generative AI coding assistants were used in developing this software. All
changes were reviewed by a maintainer before merging, and are covered by the
automated tests.

## Licence

[BSD-3-Clause](LICENSE).

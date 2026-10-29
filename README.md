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
  [self-review checklist](CONTRIBUTING.md#reviewing-your-own-pr) if you work alone.
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
├── CHANGELOG.md           what changed in each release
├── ROADMAP.md             what's planned next
├── CITATION.cff           how to cite this software
├── guidance/              the CCP-volumeEM guide, distilled into checklists
├── .agents/skills/        step-by-step procedures for AI assistants
│   ├── start-project/       set up a new repository from this template
│   ├── new-fiji-script/     write a Fiji script with a dialog, and its tests
│   ├── review-changes/      check a branch before opening a PR
│   ├── prepare-release/     choose a version and release
│   └── update-guidance/     pull in changes to the CCP-volumeEM guide
├── src/vem_project/       example package: OME-Zarr I/O, a measurement, a CLI
├── fiji/                  example Fiji script (Groovy, with Script Parameters)
├── tests/                 installation, unit, integration and Fiji tests
├── examples/              example parameters and synthetic data
├── docs/                  documentation website (MkDocs)
├── Dockerfile             container image
├── tools/                 helper scripts
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

---

## Installation

You need Python 3.11 or newer.

```bash
git clone https://github.com/ccp-volume-em/vem-project.git
cd vem-project
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Quick start

Make a small synthetic label volume and measure the objects in it:

```bash
python examples/make_example_data.py
vem-project measure examples/params.yml
```

This writes `results/example/object_volumes.csv` (volumes in nm³) and
`results/example/provenance.json` (software version, parameters, inputs). See
the [documentation](docs/index.md) for more.

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

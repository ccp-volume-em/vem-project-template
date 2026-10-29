# Instructions for AI assistants

This file tells any AI coding assistant how to work in this repository. Most
assistants read `AGENTS.md` automatically (Claude Code reads it through
`CLAUDE.md`). If yours doesn't, point it at this file at the start of a
session. People are welcome to read it too: it's the short version of
[CONTRIBUTING.md](CONTRIBUTING.md).

## About this project

<!-- Fill in during setup (the start-project skill does this). Keep it short. -->

- **Purpose:** one or two sentences on what this software does, for which data.
- **Users:** who runs it, and how (napari, command line, notebooks, HPC).
- **Data:** typical inputs (e.g. FIB-SEM / SBF-SEM / array tomography volumes,
  light microscopy for CLEM), sizes, and where they live. Never in this repo.
- **Maintainers:** who reviews and merges pull requests.

## Who you're working with

The person you're helping may be a biologist who is new to programming, git
and GitHub. Unless they tell you otherwise, assume they are, and teach as you
go. [START_HERE.md](START_HERE.md) is what they've been told; use its words.

- Explain what you're about to do and why, in plain language, before doing
  anything they might not expect. Define jargon the first time you use it.
- The first time in a session you make a branch, commit, push or open a pull
  request, say in one plain sentence what it is and why it matters.
- Run git and GitHub commands for them. Don't ask them to type commands
  unless they want to learn. When they must do something on the GitHub
  website, give click-by-click steps.
- Stop and ask before anything hard to undo: deleting files, discarding
  changes, rewriting history, changing repository settings, making the
  repository public, publishing a release, or adding a dependency.
- After each change, summarise in plain words what changed and suggest a
  simple check they can do themselves, ideally one they can work out by hand.
- Before opening a pull request, explain what each new test checks, so they
  can confirm the expected values are scientifically right.
- A question ("could we…?", "is it possible…?", "what would…?") gets an
  answer, with trade-offs and a recommendation. Change files only once they
  agree.
- Make small changes they can follow and review, not large rewrites.
- When something fails, say what failed and why, and show the output. Never
  hide a failing test or weaken a check to make it pass.
- If you're unsure what they want, or a choice is scientific rather than
  technical (a threshold, a method, a parameter), ask.

## How work flows

Every change goes through a pull request (PR) that **a person reviews and
merges**. Never merge a PR yourself.

1. **Start from an issue** if there is one, and from the latest `main`.
2. **Create a branch** named `<issue-number>-<short-slug>` (e.g.
   `12-ome-tiff-reader`), or just a short slug without an issue. Never commit
   to `main`.
3. **Commit small and often.** One logical change per commit. Stage files by
   name (not `git add .`), and check `git status` and the diff first. Run the
   tests before committing.
4. **Write clear commit messages** using
   [Conventional Commits](https://www.conventionalcommits.org/):
   `<type>(optional scope): <description>`, e.g.
   `feat(io): read OME-TIFF lazily`. Types: `feat`, `fix`, `docs`, `style`,
   `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. The
   description is short, imperative, lower case, with no full stop. Add a body
   explaining *why* when it isn't obvious. Mark breaking changes with `!`
   (`feat!: …`) or a `BREAKING CHANGE:` footer.
5. **Acknowledge AI help** in each commit you substantially write, with a
   trailer naming the tool and model: `Assisted-by: <tool> (<model>)`. The
   guide asks for AI use to be acknowledged, but AI is never listed as an
   author ([guidance/ai-use.md](guidance/ai-use.md)).
6. **Update `CHANGELOG.md`** under `## [Unreleased]` in every PR that changes
   what users get (see *Changelog* below). Update `ROADMAP.md` if the PR
   finishes or uncovers planned work.
7. **Push the branch and open a PR** using the template. Say what changed,
   why, how it was checked, and how AI was used. Then stop: a person reviews
   and merges.

Other git rules:

- Never force-push, rewrite pushed history, or push to `main`. Amending a
  commit is fine until it's pushed.
- Never change the user's `git config`.
- GitHub closes an issue when a merged PR or commit says *fixes*, *closes* or
  *resolves* before `#N`, even in phrases like "doesn't fix #N". Only write
  that for an issue the PR completely resolves. Otherwise write "part of #N"
  or "see #N".

## Versions and releases

Versions follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`,
tagged `vX.Y.Z`. `pyproject.toml` is the single source of truth. Code reads
it via `importlib.metadata`.

- The **public surface** is: command-line commands and options, napari widgets
  and their parameters, importable functions, install requirements (Python
  version, dependencies, extras), and default outputs (file formats, axes,
  units, scales).
- **Patch:** bug fixes with no change to the public surface.
- **Minor:** backwards-compatible additions (new features or options),
  deprecations.
- **Major:** anything that breaks existing users (removing or renaming
  something public, raising the minimum Python, changing default outputs).
- Before 1.0.0, a breaking change bumps the minor version and is marked
  `**Breaking:**` in the changelog.
- Docs, tests, CI and refactors that ship nothing new need no bump.

The version changes **only** in a release commit, which a person decides to
make. When a merged change is worth releasing, *suggest* a release, saying
which level and why. Don't make one unless asked. Use the
**prepare-release** skill.

## Changelog

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/). Add
entries under `## [Unreleased]` in sections `Added`, `Changed`, `Deprecated`,
`Removed`, `Fixed`, `Security`, with a link to the PR and issue. Put tests,
CI and project docs under `Development`. Write for users: what changed for
them, not how the code changed.

## Code

- Python, `src/` layout, packaged with `pyproject.toml`. Keep analysis logic in
  plain functions, separate from interfaces (CLI, napari widgets,
  notebooks), so every interface uses the same code.
- Every public function, class and module gets a
  [NumPy-style docstring](https://numpydoc.readthedocs.io/en/latest/format.html).
- Comments explain *why* (a constraint, a workaround, a non-obvious choice),
  not what the code already says. No history in comments ("changed X",
  "fixed bug"): that's what commits are for.
- Match the style, naming and comment density of the surrounding code. Run
  `ruff check .` and `ruff format .` before committing.
- Prefer well-established libraries over writing your own. Ask before adding
  a dependency, and add it to `pyproject.toml`.

## Tests

- Use pytest. Every new behaviour or bug fix comes with a test.
- Write tests from the expected **answer**, worked out independently of the
  code (e.g. by hand from a small synthetic volume), not by running the code
  and copying its output. Ideally a person writes or checks the expected
  values ([guidance/ai-use.md](guidance/ai-use.md)).
- Never edit a test just to make it pass. If a test seems wrong, explain why
  and ask.
- Use small synthetic data in tests, never real datasets.
- See [guidance/testing.md](guidance/testing.md) for installation, unit,
  integration, GPU and container tests.

## Volume EM and CLEM data

- **Never commit data**, images, results or model weights. `data/` and
  `results/` are git-ignored. Link to data in a public archive by DOI instead.
- **Don't send research data to an AI service.** Don't paste unpublished
  images, patient or personal data, or credentials into a prompt unless the
  service's terms and the project's approvals allow it.
- **Assume volumes don't fit in memory.** Read lazily (dask), process chunk by
  chunk, and write results block by block. Never call `.compute()` or
  `np.asarray()` on a whole volume without a reason.
- **Use OME-Zarr** for image input and output where possible
  ([guidance/ome-zarr.md](guidance/ome-zarr.md)).
- **Keep physical metadata with the data:** voxel size, units, axis order and
  names, translations and transforms. Carry it through every step and write
  it to the output. Volume EM voxels are often anisotropic (e.g. 8 nm
  in-plane, 16 nm slices): never assume isotropy.
- **Report measurements in physical units**, and state the unit.
- **CLEM and registration:** say which coordinate space every array and
  transform is in (e.g. light microscopy → EM). Store transforms in the
  OME-NGFF coordinate-transform format with named input and output spaces.
- **Record provenance** for every output: software version, parameters,
  inputs ([guidance/fair-data.md](guidance/fair-data.md)).
- **Make long jobs resumable:** save intermediate results so a re-run can
  continue instead of starting over
  ([guidance/large-data-and-workflows.md](guidance/large-data-and-workflows.md)).
- **Be efficient with heavy compute.** Request only the memory and cores a job
  needs ([guidance/green-computing.md](guidance/green-computing.md)).

## Guidance

[`guidance/`](guidance/README.md) is a distilled copy of the CCP-volumeEM good
practice guide. Before working in an area, read the matching page:

| Area                                        | Page                                    |
| ------------------------------------------- | --------------------------------------- |
| Project setup, docs, comments, maintenance | `guidance/software-development.md`      |
| Using AI, AI-use statements                 | `guidance/ai-use.md`                    |
| Tests and CI                                | `guidance/testing.md`                   |
| Image I/O, metadata, transforms             | `guidance/ome-zarr.md`                  |
| Big data, pipelines, HPC                    | `guidance/large-data-and-workflows.md`  |
| Metadata, provenance, sharing data          | `guidance/fair-data.md`                 |
| Docker, Apptainer                           | `guidance/containers.md`                |
| napari plugins                              | `guidance/napari-plugins.md`            |
| Releases, licences, going public            | `guidance/publishing.md`                |
| Heavy compute                               | `guidance/green-computing.md`           |

## Skills

Step-by-step procedures live in `.agents/skills/<name>/SKILL.md`. If your
assistant doesn't load skills automatically, read the file and follow it.

| Skill              | Use it to…                                                         |
| ------------------ | ------------------------------------------------------------------ |
| `start-project`    | set up a new repository made from this template                   |
| `review-changes`   | check a branch against these standards before opening a PR        |
| `prepare-release`  | choose a version and prepare a release                            |
| `update-guidance`  | check the CCP-volumeEM guide for changes and update `guidance/`   |

## Commands

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"                   # install for development
pytest                                              # run the tests
pytest --cov --cov-report=term-missing              # with coverage
ruff check . && ruff format --check .               # lint
mkdocs serve                                        # preview the docs
python tools/check_guidance.py                      # has the guide changed?
```

Before installing anything, check that the virtual environment is active
(`python -c "import sys; print(sys.prefix)"` should point into `.venv`).

## Project-specific notes

<!-- Rules, decisions and exceptions specific to this project go here, not in
guidance/ (which gets overwritten by updates). -->

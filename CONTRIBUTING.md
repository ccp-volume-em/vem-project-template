# Contributing

Thank you for helping. This page is the detailed reference for how we work.
If anything is unclear, open an issue or ask a maintainer.

**New to coding or GitHub?** Read [START_HERE.md](START_HERE.md) first. You
don't need everything on this page to get started: your AI assistant runs the
commands below for you.

AI assistants follow the same rules, summarised in [AGENTS.md](AGENTS.md).

## Where things go

| Folder | What goes there |
| --- | --- |
| `src/<package>/` | Reusable Python code that others run: the analysis, as plain functions, with thin interfaces (CLI, napari) on top |
| `fiji/` | Reusable Fiji scripts (Groovy with Script Parameters) |
| `notebooks/` | The project's own analysis: exploring data, choosing parameters, making figures. Uses the code above; outputs are stripped on commit |
| `examples/` | How to run the code: parameter files, and `make_example_data.py`, which writes a test volume for both Python (OME-Zarr) and Fiji (TIFF) |
| `tests/` | Tests of the project's code, Python and Fiji |
| `tests/repository/` | The template's checks on the repository itself. Kept up to date by `update-from-template`; don't edit |
| `tools/` | Scripts that maintain the repository (checks, updates), not analysis |
| `docs/` | The documentation site, if the project has one, and the decision log (`decisions.md`) |
| `guidance/` | The CCP-volumeEM guide, distilled. Updated by `update-guidance`; don't edit |
| `data/`, `results/` | Never in git: data stays on institute storage |

## The short version

1. Every change starts on its own **branch**, never on `main`.
2. Make **small commits** with clear messages.
3. Open a **pull request (PR)**. Tests run automatically.
4. **Someone reviews it, then a person merges it.** Ideally a colleague
   reviews it; if you work alone, review it yourself with the checklist in
   [Review](#6-review). AI assistants never merge.

## Words you'll meet

| Word                 | Meaning                                                                           |
| -------------------- | --------------------------------------------------------------------------------- |
| repository (repo)    | the project folder, with its full history                                         |
| commit               | a saved snapshot of changes, with a message saying what and why                   |
| branch               | a separate line of work, so changes don't affect `main` until they're reviewed    |
| `main`               | the reviewed, working version of the code                                         |
| pull request (PR)    | a request to merge a branch into `main`, where changes are reviewed and discussed |
| issue                | a bug report, idea or task on GitHub                                              |
| CI                   | continuous integration: automatic checks (tests, lint) that run on every PR       |
| release / tag        | a named, fixed version (e.g. `v1.2.0`) that users can install and cite            |

New to git? Try [Software Carpentry's git lesson](https://swcarpentry.github.io/git-novice/).

## One-time setup

```bash
git clone https://github.com/ccp-volume-em/vem-project.git
cd vem-project
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
python -c "import sys; print(sys.prefix)"   # should end in .venv
python -m pip install -e ".[dev]"
pre-commit install                     # checks each commit; blocks commits on main
pytest                                 # everything should pass
```

## Making a change

### 1. Start from an issue and the latest `main`

If there isn't an issue for what you want to do, consider opening one first,
so others know and can comment.

```bash
git switch main
git pull
```

### 2. Create a branch

Name it `<issue-number>-<short-description>`, or just a short description if
there's no issue:

```bash
git switch -c 12-ome-tiff-reader
```

### 3. Change, test, commit — little and often

```bash
pytest                         # tests pass?
ruff check . && ruff format .  # code tidy?
git status                     # what changed?
git diff                       # look at the changes
git add src/vem_project/io.py tests/test_io_and_cli.py   # stage files by name
git commit
```

Stage files by name rather than `git add .`, so you never commit data or
secrets by accident. As a safety net, every PR is checked for data, images,
model weights, files over 1 MB and secrets (the *Safety checks* workflow), and
pre-commit runs the data check before each commit. If a check fails, ask a
maintainer: the file has to come out of the history, not just be deleted.

#### Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat(io): read OME-TIFF files lazily

Large FIB-SEM stacks didn't fit in memory when read with imread.
Reading through tifffile's Zarr store loads only the chunks needed.

Part of #12
```

- The first line is `<type>(optional scope): <description>`: short,
  imperative ("add", not "added"), lower case, no full stop.
- Types: `feat` (new feature), `fix` (bug fix), `docs`, `test`, `refactor`
  (restructure without changing behaviour), `perf`, `style`, `build`, `ci`,
  `chore`, `revert`.
- After a blank line, explain **why** if it isn't obvious.
- A change that breaks things for existing users gets a `!`
  (`feat!: rename --input to --labels`) or a `BREAKING CHANGE:` footer.
- If an AI assistant substantially wrote the change, add a trailer:
  `Assisted-by: <tool> (<model>)`.

One commit per logical change. "Fix typo" and "add reader" are separate
commits.

### 4. Update the changelog

Add a line to [CHANGELOG.md](CHANGELOG.md) under `## [Unreleased]`, in the
right section (`Added`, `Changed`, `Fixed`, …), describing the change **for
users**, with a link to the PR. Tests, CI and developer docs go under
`Development`. Automated dependency updates from Dependabot don't need an
entry.

### 5. Open a pull request

```bash
git push -u origin 12-ome-tiff-reader
```

Then open a PR on GitHub (or `gh pr create`). Fill in the template: what
changed and why, how you checked it, how AI was used, and which issues it
relates to.

GitHub closes an issue when a merged PR says **fixes**, **closes** or
**resolves** before `#N`, even inside a sentence like "doesn't fix #12". Use
those words only for issues the PR completely resolves. Otherwise write
"part of #12".

### 6. Review

A second pair of eyes is good practice: a colleague, a maintainer, or someone
from your institute's research software group. Expect questions and
suggestions: that's normal and useful. Push more commits to the same branch to
respond. Once it's approved and the checks are green, the reviewer merges it.

Many projects have one developer, so a reviewer isn't required. If there's no
one to ask, review the PR yourself, then merge it.

**How to review**, whether it's someone else's PR or your own, is in
[REVIEWING.md](REVIEWING.md): what to check, how to spot problems in
AI-written code, how to give feedback, and a checklist for
[reviewing your own PR](REVIEWING.md#reviewing-your-own-pr).

### 7. Tidy up

Once the PR is merged, its branch has done its job: everything on it is now
in `main`. Delete it, so the list of branches only shows work in progress:

```bash
git switch main
git pull
git branch -d 12-ome-tiff-reader                # on your computer
git push origin --delete 12-ome-tiff-reader     # on GitHub, unless already gone
```

If `git branch -d` refuses, the PR may have been squash-merged: check on
GitHub that it really is merged, then use `-D`. Never delete a branch whose
PR is still open, or that has work not in `main`, without asking its owner.

## Fiji scripts

Fiji work is written as Groovy scripts with Script Parameters, in `fiji/`:
Fiji builds the dialog from the `#@` lines, and the same script runs headless
on a cluster. See [fiji/README.md](fiji/README.md). Run the Fiji tests
locally before opening a PR that changes a script (CI has no Fiji):

```bash
FIJI=/path/to/Fiji.app/fiji pytest -m fiji
```

## Tests

- Run `pytest` before every commit. CI runs it on Linux, macOS and Windows.
- Every new feature and bug fix needs a test.
- Work out expected values independently (e.g. by hand from a small synthetic
  volume), not by running the code and copying the result. This matters most
  for AI-written code.
- Never commit real data for tests. Generate small synthetic data instead.
- See [guidance/testing.md](guidance/testing.md).

## Documentation

- Every public function gets a [NumPy-style docstring](https://numpydoc.readthedocs.io/en/latest/format.html).
- Comments explain *why*, not *what*.
- The README is the starting point for users. Its install and quick-start
  text is written once, between `--8<--` markers, and the documentation site
  reuses it: edit it in the README.
- **With a documentation site** (`docs/` and `mkdocs.yml`): user guides and
  the reference built from docstrings live in `docs/`. Preview with
  `mkdocs serve`, then open <http://127.0.0.1:8000>. Pull requests check that
  it builds.
- **Without one:** the README is the user documentation. To add a site
  later, ask your AI assistant to restore it from the project template
  (`docs/`, `mkdocs.yml`, `.github/workflows/docs.yml` and the `docs` extra in
  `pyproject.toml`).

## Versions and releases

We use [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

| Change                                                         | Bump  | Example         |
| -------------------------------------------------------------- | ----- | --------------- |
| bug fix, nothing else changes for users                        | patch | 1.2.0 → 1.2.1   |
| new feature or option; existing use still works                | minor | 1.2.1 → 1.3.0   |
| breaks existing use (removed/renamed option, new output format) | major | 1.3.0 → 2.0.0   |

Before 1.0.0, breaking changes bump the minor version and are marked
**Breaking:** in the changelog. The version in `pyproject.toml` changes only
in a release PR. Maintainers decide when to release, using the
[prepare-release](.agents/skills/prepare-release/SKILL.md) steps.

## Using AI assistants

You're welcome to use AI assistants. You remain responsible for every change
you submit.

- Understand all code before you submit it. Ask the assistant to explain
  anything you don't follow.
- Check AI-written tests yourself: are the expected values actually right?
- Don't share unpublished data, personal data or credentials with an AI
  service unless its terms and your approvals allow it.
- Acknowledge AI help in commits (`Assisted-by:`) and in the PR.
- See [guidance/ai-use.md](guidance/ai-use.md).

## Code of conduct

Everyone taking part is expected to follow our
[Code of Conduct](CODE_OF_CONDUCT.md).

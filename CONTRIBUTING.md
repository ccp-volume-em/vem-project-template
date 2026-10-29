# Contributing

Thank you for helping. This page explains how we work, step by step. It's
written for people who are new to git and GitHub as well as experienced
developers. If anything is unclear, open an issue or ask a maintainer.

AI assistants follow the same rules, summarised in [AGENTS.md](AGENTS.md).

## The short version

1. Every change starts on its own **branch**, never on `main`.
2. Make **small commits** with clear messages.
3. Open a **pull request (PR)**. Tests run automatically.
4. **A person reviews and merges it.** Nobody merges their own PR unreviewed,
   and AI assistants never merge.

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
pre-commit install                     # optional: lint automatically on each commit
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
secrets by accident.

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
`Development`.

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

A maintainer, or a colleague the maintainer asks, reviews the PR. Expect
questions and suggestions: that's normal and useful. Push more commits to the
same branch to respond. Once it's approved and the checks are green, the
reviewer merges it.

**Reviewing someone else's PR?** Check that you understand the change, that
it's tested, and that it follows [AGENTS.md](AGENTS.md) and
[guidance/](guidance/README.md). Run it if in doubt.

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
- User documentation lives in `docs/` and is built with MkDocs:
  `mkdocs serve`, then open <http://127.0.0.1:8000>.

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

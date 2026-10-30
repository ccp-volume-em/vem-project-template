---
name: update-from-template
description: Bring improvements from the CCP-volumeEM project template (new rules, skills, checks, workflows, guidance) into a project made from it, keeping the project's own changes. Use when asked to update from the template, or to check whether the project is up to date with it.
---

# Update from the project template

A project made from the template doesn't receive the template's later
improvements by itself. `.github/tools/check_template.py` works out which template
version the project is based on (from `.github/template.json`, or by asking
GitHub) and what has changed since. Explain each step to the user as you go.

## 1. See what changed

```bash
GITHUB_TOKEN=$(gh auth token) python .github/tools/check_template.py
```

`GITHUB_TOKEN` lets it read a private template; without `gh`, the user can
set a personal access token instead.

- Exit 0: up to date (or this is the template itself). Tell the user and stop.
- Exit 2: it couldn't reach the template. Report the error. If the template is
  private, the user needs access to it.
- Exit 1: it lists the **shared files** that changed (rules, skills, checks,
  workflows, guidance) and the **project files** that changed in the template
  (example code, README, `pyproject.toml`, changelog), and links to the full
  comparison.

Read the template's release notes for the versions in between
(`https://github.com/<template>/releases`), and summarise for the user, in
plain words, what's new and why it matters to them. Ask before going on.

## 2. Merge the shared files on a branch

Create a branch from the latest `main`: `update-from-template-<version or date>`.
Then fetch the old and new template versions of the shared files into a
folder **outside** the repository:

```bash
GITHUB_TOKEN=$(gh auth token) python .github/tools/check_template.py --fetch /tmp/template-update
```

For each shared file:

- **Changed in the template, exists here:** merge the template's change into
  the project's version, keeping the project's own edits:

  ```bash
  git merge-file -L this-project -L template-before -L template-after \
      <file> /tmp/template-update/base/<file> /tmp/template-update/latest/<file>
  ```

  Exit 0 means a clean merge. A positive exit means that many conflicts,
  marked `<<<<<<<` in the file. Resolve each one with the user: explain both
  sides and ask which to keep, or combine them. Never silently drop the
  project's own text, such as *About this project* and *Project-specific
  notes* in `AGENTS.md`.
- **New in the template:** copy it from `latest/`. Replace the template's
  example names (`vem-project`, `vem_project`) with the project's own.
- **Removed from the template:** ask the user before removing it here.
- **The project deleted a file the template changed:** ask whether they
  want it back, and don't restore it unasked. Files of optional parts the
  project left out (the docs site, container, Fiji scripts, notebooks) are
  already skipped by `check_template.py`; to add one, use the `add-part`
  skill.

For **project files**, don't merge anything automatically. Point out changes
the user may want (e.g. a new dependency or test pattern) and offer to make
them separately.

## 3. Check and record

1. Install and run everything: `python -m pip install -e ".[dev]"`, then
   `pre-commit install`, `pytest`, `ruff check .`. Fix anything the update
   broke, and say what.
2. Record the new template version:
   `GITHUB_TOKEN=$(gh auth token) python .github/tools/check_template.py --record`.
3. Add a `CHANGELOG.md` entry under `[Unreleased]` → `Development`, e.g.
   "Updated from the project template (v0.3.0): …", listing what users of
   the project will notice, if anything.

## 4. Commit and open a pull request

Commit in logical steps (e.g. `chore: update from template v0.3.0`), push,
and open a PR that lists what came from the template, which conflicts were
resolved and how, and what was deliberately left out. Link the template
comparison. Then stop: a person reviews and merges it.

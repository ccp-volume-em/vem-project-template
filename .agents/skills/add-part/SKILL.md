---
name: add-part
description: Add an optional part that the project left out at setup (the documentation website, a container for Docker or Apptainer, Fiji scripts, or Jupyter notebooks), copied from the project template and adapted. Use when the user wants one of these, e.g. "add a docs site", "containerise this", "add Docker", "I want to use notebooks", or "add Fiji scripts".
---

# Add an optional part

Projects start small. The optional parts are described in
`.github/template-parts.toml`, and `tools/parts.py` adds or removes their
files the same way for every part. Explain each step in plain words.

## 1. Check and ask

Run `python tools/parts.py list` to see which parts the project has. Read the
part's entry in `.github/template-parts.toml`, and talk it through with the
user: its `question` and `recommend` say what it's for. If it doesn't suit
the project's shape (`shapes`), say so and stop, unless they still want it.
For the container, also read `guidance/containers.md`; for the docs site,
`guidance/software-development.md`.

## 2. Add the files

On a branch (e.g. `add-container`):

```bash
GITHUB_TOKEN=$(gh auth token) python tools/parts.py add <part>
```

It copies the part's files from the template version in
`.github/template.json`, so they match the project's other template files
(`update-from-template` brings later changes). It replaces the template's
example names with the project's, never overwrites an existing file, and
removes the *Left out* note from `AGENTS.md`. Without `gh`, the token is only
needed for a private template.

## 3. Make the edits

The script prints the part's `edits`: the changes made to other files when
it was left out. Undo each one, using the template's version of that file
as a guide (`https://github.com/<template>/blob/<commit>/<file>`, from
`.github/template.json`), adapted to the project: its names, its own text,
and the parts it has. Then do the part's `after_add` steps. Read the new
files and check the template's example names were all replaced
(`git grep -n -i "vem.project"`).

## 4. Check, record, open a PR

- Run the tests (`pytest`). For the docs site, also `mkdocs build --strict`;
  for the container, `docker build` if Docker is installed (otherwise the
  *Container* check on the pull request builds it).
- Add a `CHANGELOG.md` entry under `Added`, e.g. "A container image, to run
  the tool with Docker or Apptainer". A new way to use the tool means a minor
  release; a docs site or notebooks for the project's own work need none.
- Commit (`feat: add a container image`), push and open a PR, explaining
  what the part adds and anything the user must decide or set up (e.g. turning
  on GitHub Pages, or publishing container images).

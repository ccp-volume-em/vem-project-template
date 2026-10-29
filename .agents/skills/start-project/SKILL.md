---
name: start-project
description: Set up a new repository created from the CCP-volumeEM project template, replacing the example package name and placeholders, choosing a licence and filling in project details. Use once, right after creating a repository from the template, or when the user asks to "set up", "rename" or "personalise" the project.
---

# Set up a new project from the template

The user has just created a repository from the template. Walk them through
setup in a conversation. Explain each step briefly, ask the questions below,
and don't assume answers. They may be new to coding and GitHub: use the plain
language and vocabulary of `START_HERE.md`, and explain each choice's
consequences rather than just listing options.

## 1. Ask

1. **Name.** What's the project called? Suggest a distribution name (lower
   case, hyphens, e.g. `fibsem-mito-seg`) and the matching import name
   (underscores, `fibsem_mito_seg`). Check PyPI to see if the name is taken
   (`https://pypi.org/project/<name>/`) if they might publish there.
2. **Purpose.** One or two sentences: what does it do, for which data?
3. **Shape.** Command-line tool, napari plugin, Fiji scripts, notebooks, a
   library, or a mix? Fiji scripts are Groovy with Script Parameters (see
   `fiji/README.md`); if they won't use Fiji, the `fiji/` folder and its tests
   can go. If napari, point them to `guidance/napari-plugins.md` and the official
   napari plugin template, and explain that the analysis code in `src/` can be
   reused by the plugin.
4. **People.** Authors (names, ORCIDs, affiliations), and whether anyone
   else will review pull requests. Recommend a reviewer if they can find
   one, but a sole developer is fine: explain that they'll review their own
   PRs with the checklist in `CONTRIBUTING.md` (*Reviewing your own PR*).
5. **Licence.** The template uses BSD-3-Clause, common in scientific Python and
   napari. Explain the options in `guidance/publishing.md` briefly, and
   recommend they check with their institution if unsure.
6. **Example code.** Keep the example (`io.py`, `measure.py`, `cli.py`) as a
   starting point, or remove it?

## 2. Make the changes on a branch

Create a branch `setup-project`. Then:

1. **Rename** everywhere: `vem-project` → distribution name, `vem_project` →
   import name, including the `src/vem_project/` folder (use `git mv`). Search
   the whole repository, including `.github/`, `docs/`, `mkdocs.yml`,
   `Dockerfile`, `tox.ini`, tests and examples:
   `git grep -n -i "vem.project"`.
2. **Repository URLs:** replace `ccp-volume-em/vem-project` with the real
   `owner/repo` (from `git remote get-url origin`).
3. **Descriptions and authors:** `pyproject.toml` (`description`, `authors`),
   `CITATION.cff` (`title`, `abstract`, `authors`), `LICENSE` (copyright line),
   `README.md` (title, description; remove the *About this template* section),
   `docs/index.md`, and `mkdocs.yml` (`site_name`, URLs).
4. **Licence:** if they chose another, replace `LICENSE` with the unmodified
   text from <https://choosealicense.com>, and update `license` in
   `pyproject.toml` and `CITATION.cff` with its SPDX identifier.
5. **AGENTS.md:** fill in *About this project*.
6. **START_HERE.md:** keep it for future collaborators, but rewrite *Your
   first session* for joining this project rather than copying the template:
   how to get access (and from whom), opening the repository in an AI
   assistant, and a first thing to say, such as "Read `AGENTS.md` and
   `START_HERE.md`, then explain what this project does and how it's
   organised." Name the project's reviewers, if any, in *What you need*.
7. **Example code:** if they don't want it, remove the modules, tests,
   `examples/` and docs pages that use it, and the example Fiji script if
   they don't use Fiji (with `tests/test_fiji_scripts.py`). Keep
   `tests/test_installation.py` and `tests/test_project_files.py`, and adapt
   them.
8. **CHANGELOG.md:** leave just the `## [Unreleased]` heading, with an
   `Added` entry describing the initial project.
9. **ROADMAP.md:** replace the template's items with the user's first goals.
   **docs/decisions.md:** remove the template's example entry. If the user
   has already made choices (e.g. the method), record them as the first
   entries, with their reasons.

Then check nothing was missed (`git grep -n -i "vem.project\|Your Name\|you@example"`),
install (`python -m pip install -e ".[dev]"` in a fresh virtual environment)
and run `pytest` and `ruff check .`. Commit in logical steps, open a PR, and
ask the reviewer they named to review it. With no reviewer, walk them through
self-review instead (`AGENTS.md`, *How work flows*).

## 3. Repository settings to suggest

Explain these, and offer to do them with `gh` if it's installed:

- **Protect `main`:** require a pull request and passing checks before
  merging. Settings → Rules → Rulesets. Require an approving review only if
  someone else reviews: GitHub doesn't let authors approve their own PRs, so
  that rule would block a sole developer. On a free GitHub plan rulesets are
  only enforced on public repositories. For private ones, the rule is a team
  convention.
- **Delete branches after merging:** Settings → General → *Automatically
  delete head branches*, so merged branches don't pile up on GitHub
  (`gh repo edit --delete-branch-on-merge`). Local copies are still tidied by
  the AI after each merge.
- **Dependabot alerts and security updates:** Settings → Code security.
- **Issues** on, and labels for `bug`, `enhancement`, `documentation`.
- **GitHub Pages** (for the docs site): Settings → Pages → *Deploy from a
  branch* → `gh-pages`, once the repository is public or on a paid plan.
- **Zenodo:** connect the repository at <https://zenodo.org/account/settings/github/>
  before the first release, so each release gets a DOI.
- **Community forum:** if users will need help, choose one forum (e.g.
  [image.sc](https://forum.image.sc/)) and link it in the README.

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
3. **Shape.** Which of these will the project be? This decides what to keep
   (see *Where things go* in `AGENTS.md`):
   - **Python** (a command-line tool, library or napari plugin), with or
     without Fiji scripts;
   - **Fiji scripts only** (Groovy with Script Parameters, see
     `fiji/README.md`). Python is then used only for the tests and checks.

   If napari, point them to `guidance/napari-plugins.md` and the official
   napari plugin template, and explain that the analysis code in `src/` can be
   reused by the plugin.
   **Documentation site?** Ask whether other people will install and use the
   software. If so, keep the documentation website (`docs/`, `mkdocs.yml`). It
   adds a user guide and a reference built from the docstrings, and is
   published once the repository is public. If not (e.g. a private analysis or
   a few scripts), recommend removing it: the README is enough, and the site
   can be added back later.
4. **People.** Authors (names, ORCIDs, affiliations), and whether anyone
   else will review pull requests. Recommend a reviewer if they can find
   one, but a sole developer is fine: explain that they'll review their own
   PRs with the checklist in `REVIEWING.md` (*Reviewing your own PR*).
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
7. **Example code, by shape.** Never touch `tests/repository/` (the
   template's checks), `tools/` or `docs/decisions.md`.
   - **Python, keeping the example as a starting point:** rename it (step 1)
     and adapt it.
   - **Python, replacing the example:** replace the modules in `src/`, their
     tests in `tests/`, and `examples/params.yml`. Keep
     `tests/test_installation.py` (adapted) and `examples/make_example_data.py`
     until they have their own test data.
   - **Notebooks:** keep `notebooks/` and its README for the project's own
     analysis. Delete the example notebook and `tests/test_example_notebook.py`
     once they have notebooks of their own, or straight away for a Fiji-only
     project (it uses the Python package).
   - **No Fiji:** delete `fiji/`, `tests/test_fiji_scripts.py`, and the
     *Fiji scripts* section of `CONTRIBUTING.md` (it links to `fiji/`). Keep
     the Fiji rules in `AGENTS.md` and the `new-fiji-script` skill, so Fiji
     scripts can be added later.
   - **Fiji scripts only:**
     - delete `src/`, the Python tests (`tests/test_installation.py`,
       `test_io_and_cli.py`, `test_measure.py`, `test_examples.py`, and
       `test_fiji_and_python_agree_on_the_example_data` in
       `tests/test_fiji_scripts.py`), `examples/params.yml`, the OME-Zarr part
       of `examples/make_example_data.py`, `Dockerfile`, `.dockerignore` and
       `.github/workflows/container.yml`;
     - in `pyproject.toml`, set `dependencies = []`, remove
       `[project.scripts]` and `[tool.coverage.run]`, and add the block below
       under `[build-system]`, so `pip install -e ".[dev]"` still installs the
       test tools:

       ```toml
       # No Python package: the project is Fiji scripts. Python is only used
       # for the tests and tools, so build an empty package pip can install.
       [tool.hatch.build.targets.wheel]
       bypass-selection = true
       ```

     - in the documentation site, if kept, delete `docs/reference.md` and its
       entries in `mkdocs.yml` and `docs/index.md`, and rewrite
       `docs/usage.md` for the Fiji scripts;
     - rewrite the README's *Quick start* for Fiji, from `fiji/README.md`.
8. **CHANGELOG.md:** remove the template's release history, leaving just
   the `## [Unreleased]` heading, with an `Added` entry describing the
   initial project, and one link line at the bottom:
   `[Unreleased]: https://github.com/<owner>/<repo>/commits/main`.
9. **ROADMAP.md:** replace the template's items with the user's first goals.
   **docs/decisions.md:** remove the template's example entry. If the user
   has already made choices (e.g. the method), record them as the first
   entries, with their reasons.
10. **Template version:** record which template version the project came
    from, so later template improvements can be merged in with the
    `update-from-template` skill:
    `GITHUB_TOKEN=$(gh auth token) python tools/check_template.py --init`.
    Commit the resulting `.github/template.json`.
11. **Documentation site:** if they don't want one, delete `mkdocs.yml`,
    `.github/workflows/docs.yml` and every page in `docs/` except
    `docs/decisions.md`; remove the `docs` extra from `pyproject.toml` (and
    from the `dev` extra); remove the `mkdocs serve` line from `AGENTS.md`;
    and in `CONTRIBUTING.md` → *Documentation*, keep only the bullets for
    projects without a site. The README is then the user documentation.

Then check nothing was missed (`git grep -n -i "vem.project\|Your Name\|you@example"`),
install (`python -m pip install -e ".[dev]"` in a fresh virtual environment),
then run `pre-commit install`. Explain that this adds checks that run before
every commit: tidy code, no data files, and no commits straight to `main`.
Then run `pytest` and `ruff check .`. Commit in logical steps, open a PR, and
ask the reviewer they named to review it. With no reviewer, walk them through
self-review instead (`AGENTS.md`, *How work flows*).

## 3. Repository settings to suggest

Explain these, and offer to do them with `gh` if it's installed:

- **Protect `main`.** Explain in plain words: the pre-commit hook stops
  commits to `main` only on computers where it's installed, and AI
  assistants can ignore instructions. A rule on GitHub itself makes sure
  every change reaches `main` through a pull request, with the tests and
  safety checks passing, whoever makes it and however. Settings aren't copied
  from the template, so each project adds the rule itself.
  `.github/rulesets/main.json` holds the rule: a pull request is needed,
  `lint`, `all-tests`, `no-data-files` and `no-secrets` must pass, and `main`
  can't be force-pushed or deleted. Approvals aren't required, because
  GitHub doesn't let authors approve their own pull requests, which would
  block a sole developer; if someone else will review, offer to set
  `required_approving_review_count` to 1. Add it after the setup PR is
  merged, so the `all-tests` check exists on `main`:

  ```bash
  gh api -X POST repos/<owner>/<repo>/rulesets --input .github/rulesets/main.json
  ```

  On GitHub's free plan, rules only work on public repositories (the command
  fails with *Upgrade to GitHub Pro or make this repository public*). For a
  private repository, explain that the pre-commit hook and the habit of
  always using a pull request are the only guards, and add the rule when the
  repository goes public. If they rename or remove one of those checks in
  `.github/workflows/`, update the rule too, or pull requests can't be
  merged (a test checks the file agrees with the workflows).
- **Delete branches after merging:** Settings → General → *Automatically
  delete head branches*, so merged branches don't pile up on GitHub
  (`gh repo edit --delete-branch-on-merge`). Local copies are still tidied by
  the AI after each merge.
- **Dependabot alerts and security updates:** Settings → Code security.
- **Issues** on, and labels for `bug`, `enhancement`, `documentation`.
- **Documentation site on GitHub Pages** (if they kept the site): GitHub's
  free plan only serves sites for public repositories. Once the repository
  is public, the *Docs* workflow publishes the site to a `gh-pages` branch on
  every merge to `main`. After its first run, turn it on in Settings →
  Pages → *Deploy from a branch* → `gh-pages`, folder `/ (root)`. The site
  appears at `https://<owner>.github.io/<repo>/`; check `site_url` in
  `mkdocs.yml` matches.
- **Zenodo:** connect the repository at <https://zenodo.org/account/settings/github/>
  before the first release, so each release gets a DOI.
- **Community forum:** if users will need help, choose one forum (e.g.
  [image.sc](https://forum.image.sc/)) and link it in the README.

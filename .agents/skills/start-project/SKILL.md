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
4. **Optional parts.** Projects start small, and anything left out can be
   added later with the `add-part` skill. Run `python tools/parts.py list`.
   For each part whose `shapes` (in `.github/template-parts.toml`) include
   theirs, ask its `question` in plain words and give its `recommend`
   advice. Unless there's a reason to include a part, recommend leaving it
   out: every file they keep is one more to understand. Fiji-only projects
   always keep `fiji`.
5. **People.** Authors (names, ORCIDs, affiliations), and whether anyone
   else will review pull requests. Recommend a reviewer if they can find
   one, but a sole developer is fine: explain that they'll review their own
   PRs with the checklist in `REVIEWING.md` (*Reviewing your own PR*).
6. **Licence.** The template uses BSD-3-Clause, common in scientific Python and
   napari. Explain the options in `guidance/publishing.md` briefly, and
   recommend they check with their institution if unsure.
7. **Example code.** Keep the example (`io.py`, `measure.py`, `cli.py`) as a
   starting point, or remove it?

## 2. Make the changes on a branch

Create a branch `setup-project`. Then:

1. **Template version:** record which template version the project came
   from. Updates from the template (`update-from-template`) and adding parts
   later (`add-part`) both start from it:
   `GITHUB_TOKEN=$(gh auth token) python tools/check_template.py --init`.
2. **Leave out the parts they don't want**, one at a time:
   `python tools/parts.py remove <part>`. It deletes the part's files,
   records the choice in `.github/template.json` and under *Project-specific
   notes* in `AGENTS.md` (so updates skip it, and future contributors know
   it was deliberate), and prints the edits to make in other files. Make
   them. Commit each part separately, e.g. `chore: leave out the container`.
3. **Rename** everywhere: `vem-project` → distribution name, `vem_project` →
   import name, including the `src/vem_project/` folder (use `git mv`). Search
   the whole repository, including `.github/`, `docs/`, `mkdocs.yml`,
   `Dockerfile`, tests and examples: `git grep -n -i "vem.project"`. Leave
   links to the template itself (`ccp-volume-em/vem-project-template`, e.g.
   in `START_HERE.md` and `.github/template.json`) as they are: a plain
   find-and-replace of `vem-project` would break them.
4. **Repository URLs:** replace `ccp-volume-em/vem-project` with the real
   `owner/repo` (from `git remote get-url origin`), again leaving links to
   `ccp-volume-em/vem-project-template` alone. Two places point at the
   template on purpose and must be changed to the new repository: the
   *Tests* badge at the top of `README.md`, and `site_url`, `repo_url` and
   `repo_name` in `mkdocs.yml` (if the site is kept). Then delete the
   *Example address* notes, from each `<!-- template-example:start -->` to
   its `end` marker (`git grep -n template-example`): they tell visitors to
   the template that these addresses are examples.
5. **Descriptions and authors:** `pyproject.toml` (`description`, `authors`),
   `CITATION.cff` (`title`, `abstract`, `authors`), `LICENSE` (copyright line),
   `README.md` (title, description; remove the *About this template* section,
   and the template's status notice between the `template-status` markers).
   If the site is kept: `docs/index.md` (the same status notice) and
   `mkdocs.yml` (`site_name`). Always delete `overrides/`, and the
   `custom_dir` line in `mkdocs.yml` if there is one: they add the banner
   saying the site is the template's example.
6. **Licence:** if they chose another, replace `LICENSE` with the unmodified
   text from <https://choosealicense.com>, and update `license` in
   `pyproject.toml` and `CITATION.cff` with its SPDX identifier.
7. **AGENTS.md:** fill in *About this project*.
8. **START_HERE.md:** keep it for future collaborators, but rewrite *Your
   first session* for joining this project rather than copying the template:
   how to get access (and from whom), opening the repository in an AI
   assistant, and a first thing to say, such as "Read `AGENTS.md` and
   `START_HERE.md`, then explain what this project does and how it's
   organised." Name the project's reviewers, if any, in *What you need*.
9. **Example code, by shape.** Never touch `tests/repository/` (the
   template's checks), `tools/` or `docs/decisions.md`.
   - **Python, keeping the example as a starting point:** rename it (step 3)
     and adapt it.
   - **Python, replacing the example:** replace the modules in `src/`, their
     tests in `tests/`, and `examples/params.yml`. Keep
     `tests/test_installation.py` (adapted) and `examples/make_example_data.py`
     until they have their own test data.
   - **Fiji scripts only:**
     - delete `src/`, the Python tests (`tests/test_installation.py`,
       `test_io_and_cli.py`, `test_measure.py`, `test_examples.py`, and
       `test_fiji_and_python_agree_on_the_example_data` in
       `tests/test_fiji_scripts.py`), `examples/params.yml`, and the OME-Zarr
       part of `examples/make_example_data.py`;
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
10. **CHANGELOG.md:** remove the template's release history, leaving just
    the `## [Unreleased]` heading, with an `Added` entry describing the
    initial project, and one link line at the bottom:
    `[Unreleased]: https://github.com/<owner>/<repo>/commits/main`.
11. **ROADMAP.md:** replace the template's items with the user's first goals.
    **docs/decisions.md:** remove the template's example entry. If the user
    has already made choices (e.g. the method), record them as the first
    entries, with their reasons.

Then check nothing was missed (`git grep -n -i "vem.project\|Your Name\|you@example"`;
the only matches left should be links to `vem-project-template`, and
`git grep -n "template-status\|template-example"` should find nothing),
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

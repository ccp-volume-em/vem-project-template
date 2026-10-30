# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/).
Sections: Added, Changed, Deprecated, Removed, Fixed, Security, and
Development (tests, CI and developer docs).

## [Unreleased]

### Added

- The container is optional: setup asks whether the project will be
  containerised and removes it if not, and the new `add-container` skill
  adds it back later. Setup records each part it leaves out in
  `AGENTS.md`, so `update-from-template` doesn't offer it back
  ([#24](https://github.com/ccp-volume-em/vem-project-template/pull/24)).
- Notes next to links and commands that use the example project's
  address, saying they're examples that setup fills in. The template's
  documentation site links to the template
  ([#23](https://github.com/ccp-volume-em/vem-project-template/pull/23)).
- The template's documentation site says on every page that it's an example
  of a project's site, not a guide to the template, and links to the README
  and START_HERE ([#21](https://github.com/ccp-volume-em/vem-project-template/pull/21)).
- A rule protecting `main` (`.github/rulesets/main.json`): changes arrive
  only through pull requests whose tests and safety checks pass. The
  `start-project` skill adds it to new projects. A single `all-tests` check
  sums up the test matrix for it
  ([#19](https://github.com/ccp-volume-em/vem-project-template/pull/19)).
- Work-in-progress notices in the README, START_HERE.md and the documentation
  site, while the template is being tested
  ([#18](https://github.com/ccp-volume-em/vem-project-template/pull/18)).
- A "Where things go" guide to the folders, organised by role, and
  start-project instructions for Python, Fiji-only and no-Fiji projects
  ([#16](https://github.com/ccp-volume-em/vem-project-template/pull/16)).
- `examples/make_example_data.py` makes the example volume for both the Python
  tool (OME-Zarr) and Fiji (TIFF) ([#16](https://github.com/ccp-volume-em/vem-project-template/pull/16)).
- `notebooks/` for the project's own analysis, with an example notebook and
  outputs stripped automatically on commit; a `notebooks` extra installs
  JupyterLab ([#17](https://github.com/ccp-volume-em/vem-project-template/pull/17)).

### Changed

- The documentation site is optional: setup asks whether others will use the
  software and removes the site if not, keeping the decision log. The
  install and quick-start text is written once, in the README, and reused by
  the site ([#15](https://github.com/ccp-volume-em/vem-project-template/pull/15)).
- The template's checks on the repository moved to `tests/repository/`
  ([#16](https://github.com/ccp-volume-em/vem-project-template/pull/16)).

### Fixed

- The README's *Tests* badge shows the template's own tests, instead of a
  broken image. The `start-project` skill points it at the new repository,
  and keeps links to the template intact when renaming
  ([#22](https://github.com/ccp-volume-em/vem-project-template/pull/22)).
- The pre-commit YAML check no longer rejects `mkdocs.yml`
  ([#21](https://github.com/ccp-volume-em/vem-project-template/pull/21)).
- The Fiji script writes large volumes as plain numbers, not in scientific
  notation ([#16](https://github.com/ccp-volume-em/vem-project-template/pull/16)).

### Development

- Test runs on `main` are no longer cancelled when another merge follows
  quickly, so the tests badge doesn't show failing for a cancelled run
  ([#22](https://github.com/ccp-volume-em/vem-project-template/pull/22)).

## [0.1.0] - 2026-10-29

First release of the CCP-volumeEM project template.

**AI use:** developed with AI assistance (Claude Code, Claude Opus 5.5) from
the maintainer's design and requests. Every change went through a pull
request that the maintainer merged, and the code is covered by the automated
tests. The checklists in `guidance/` were distilled by AI from the
CCP-volumeEM guide and link back to each source page.

### Added

- The project template: a Python package with an example OME-Zarr
  measurement tool and command-line interface, tests, CI on Linux, macOS and
  Windows, a documentation site, a container image, release automation,
  `CITATION.cff`, and instructions (`AGENTS.md`) and skills for any AI
  assistant ([#1](https://github.com/ccp-volume-em/vem-project-template/pull/1)).
- `START_HERE.md`: a plain-language guide for researchers new to coding and
  GitHub, covering the key words, how a change happens, what to say to an AI
  assistant, and what to check before asking for review
  ([#3](https://github.com/ccp-volume-em/vem-project-template/pull/3)).
- Fiji script `fiji/measure_object_volumes.groovy`: the physical volume of each
  object in a 3D label image, with a dialog built from Script Parameters, a
  headless mode for batch and HPC runs, and a provenance record ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- `new-fiji-script` skill: Fiji work is written as Groovy scripts with Script
  Parameters unless asked otherwise ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- `REVIEWING.md`: how to review a pull request, someone else's or your own,
  including the science to check, problems typical of AI-written code, and
  GitHub's review tools ([#8](https://github.com/ccp-volume-em/vem-project-template/pull/8)).
- Safety checks that block data, images, model weights, files over 1 MB and
  secrets: before each commit (pre-commit) and on every pull request
  ([#9](https://github.com/ccp-volume-em/vem-project-template/pull/9)).
- `docs/decisions.md`: a log of scientific and analysis choices and the
  reasons for them, which AI assistants keep up to date with the user
  ([#12](https://github.com/ccp-volume-em/vem-project-template/pull/12)).
- `update-from-template` skill and `tools/check_template.py`: bring the
  template's later improvements into a project, keeping the project's own
  edits; new projects record which template version they came from
  ([#11](https://github.com/ccp-volume-em/vem-project-template/pull/11)).

### Changed

- Review by someone other than the author is now recommended rather than
  required, since many projects have one developer. `CONTRIBUTING.md` gains a
  self-review checklist, `START_HERE.md` a plain-language version, and
  `AGENTS.md` tells AI assistants how to support an honest self-review. AI
  assistants still never merge
  ([#7](https://github.com/ccp-volume-em/vem-project-template/pull/7)).
- `AGENTS.md` asks AI assistants to teach as they go: explain git and GitHub
  steps the first time, run commands for the user, and stop before anything
  hard to undo ([#3](https://github.com/ccp-volume-em/vem-project-template/pull/3)).
- AI assistants delete a branch, locally and on GitHub, once its pull request
  is merged ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- Automated dependency updates (Dependabot) no longer need changelog entries
  ([#6](https://github.com/ccp-volume-em/vem-project-template/pull/6)).
- A pre-commit hook blocks commits made directly on `main`, and new projects
  install the hooks during setup ([#10](https://github.com/ccp-volume-em/vem-project-template/pull/10)).

### Fixed

- Release notes no longer include the link lines at the bottom of
  `CHANGELOG.md` ([#6](https://github.com/ccp-volume-em/vem-project-template/pull/6)).

### Development

- Tests check every Fiji script declares Script Parameters, and run the
  scripts on synthetic images when `FIJI` points at a Fiji launcher; `tifffile`
  added to the `test` extra ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- The template itself is released from `vX.Y.Z` tags with notes only, keeping
  `pyproject.toml` at `0.0.0` for new projects ([#6](https://github.com/ccp-volume-em/vem-project-template/pull/6)).
- Tests check that relative links and anchors in Markdown files resolve
  ([#8](https://github.com/ccp-volume-em/vem-project-template/pull/8)).

[Unreleased]: https://github.com/ccp-volume-em/vem-project-template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ccp-volume-em/vem-project-template/releases/tag/v0.1.0

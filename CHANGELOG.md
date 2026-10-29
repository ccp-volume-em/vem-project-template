# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/).
Sections: Added, Changed, Deprecated, Removed, Fixed, Security, and
Development (tests, CI and developer docs).

## [Unreleased]

### Added

- Project created from the CCP-volumeEM project template.
- `START_HERE.md`: a plain-language guide for researchers new to coding and
  GitHub, covering the key words, how a change happens, what to say to an AI
  assistant, and what to check before asking for review
  ([#3](https://github.com/ccp-volume-em/vem-project-template/pull/3)).
- Fiji script `fiji/measure_object_volumes.groovy`: the physical volume of each
  object in a 3D label image, with a dialog built from Script Parameters, a
  headless mode for batch and HPC runs, and a provenance record ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- `new-fiji-script` skill: Fiji work is written as Groovy scripts with Script
  Parameters unless asked otherwise ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).

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

### Fixed

- Release notes no longer include the link lines at the bottom of
  `CHANGELOG.md` ([#6](https://github.com/ccp-volume-em/vem-project-template/pull/6)).

### Development

- Tests check every Fiji script declares Script Parameters, and run the
  scripts on synthetic images when `FIJI` points at a Fiji launcher; `tifffile`
  added to the `test` extra ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- The template itself is released from `vX.Y.Z` tags with notes only, keeping
  `pyproject.toml` at `0.0.0` for new projects ([#6](https://github.com/ccp-volume-em/vem-project-template/pull/6)).

[Unreleased]: https://github.com/ccp-volume-em/vem-project/commits/main

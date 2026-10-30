# Roadmap

What's left to do, most important first. Finished work moves to
[CHANGELOG.md](CHANGELOG.md). Link each item to its issue.

## Next

- [ ] Get a DOI for the template: release v0.2.0 and check Zenodo archives
      it (the release is made by GitHub Actions; Zenodo is connected), then
      add the concept DOI and badge to the README's *Citing the template*
      ([#31](https://github.com/ccp-volume-em/vem-project-template/pull/31)).
- [ ] Once testing is finished, remove the work-in-progress notices from
      `README.md`, `START_HERE.md` and `docs/index.md`, the matching step
      in the `start-project` skill, and the "Work in progress, being tested"
      prefix on the repository's description (a GitHub setting)
      ([#18](https://github.com/ccp-volume-em/vem-project-template/pull/18)).
- [ ] Replace the example measurement with the project's first real analysis.
- [ ] Decide the supported interfaces (CLI, napari plugin, Fiji scripts,
      notebooks).

- [ ] Ask testers what they found intimidating or confusing on first
      opening a project, and simplify further.

## Later

- [ ] A simpler starting point for Fiji-only projects, with no Python for the
      user to install: Groovy scripts and tests, expected results in CSV,
      and Python only inside GitHub's checks. Probably a second template
      (e.g. `vem-fiji-template`) synced from this one for shared files.
      Needs the Fiji tests running in CI first. Trade-off: no checks on the
      user's own computer before each commit, so it suits public
      repositories best.
- [ ] More optional parts, added the same way (`.github/template-parts.toml`):
      e.g. a napari plugin, or publishing to PyPI.

- [ ] Run the Fiji script tests in CI (e.g. a job that downloads Fiji):
      GitHub Actions skips them today, so they only run locally
      ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- [ ] Try the `update-from-template` skill on a real project made from the
      template ([#11](https://github.com/ccp-volume-em/vem-project-template/pull/11)).
- [ ] Check for template updates on a schedule, as for the guide. Possible
      now the template is public: a project's Actions can read it without a
      token ([#11](https://github.com/ccp-volume-em/vem-project-template/pull/11)).
- [ ] Review the docs tooling: Material for MkDocs reaches end of life in
      May 2027; its successor is [Zensical](https://zensical.org/).

## Open questions

- Questions that need a decision, with who decides.

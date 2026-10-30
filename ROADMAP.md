# Roadmap

What's left to do, most important first. Finished work moves to
[CHANGELOG.md](CHANGELOG.md). Link each item to its issue.

## Next

- [ ] Once testing is finished, remove the work-in-progress notices from
      `README.md`, `START_HERE.md` and `docs/index.md`, the matching step
      in the `start-project` skill, and the "Work in progress, being tested"
      prefix on the repository's description (a GitHub setting)
      ([#18](https://github.com/ccp-volume-em/vem-project-template/pull/18)).
- [ ] Replace the example measurement with the project's first real analysis.
- [ ] Decide the supported interfaces (CLI, napari plugin, Fiji scripts,
      notebooks).

## Later

- [ ] First release (`v0.1.0`) archived on Zenodo.
- [ ] Publish the documentation site: the Docs workflow now builds it into
      the `gh-pages` branch; turn on GitHub Pages from that branch.
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

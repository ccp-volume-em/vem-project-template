# Roadmap

What's left to do, most important first. Finished work moves to
[CHANGELOG.md](CHANGELOG.md). Link each item to its issue.

## Next

- [ ] Once the template is public, add the rule protecting `main`:
      `gh api -X POST repos/ccp-volume-em/vem-project-template/rulesets --input .github/rulesets/main.json`
      ([#19](https://github.com/ccp-volume-em/vem-project-template/pull/19)).
- [ ] Replace the example measurement with the project's first real analysis.
- [ ] Decide the supported interfaces (CLI, napari plugin, Fiji scripts,
      notebooks).

## Later

- [ ] First release (`v0.1.0`) archived on Zenodo.
- [ ] Publish the documentation site.
- [ ] Run the Fiji script tests in CI (e.g. a job that downloads Fiji):
      GitHub Actions skips them today, so they only run locally
      ([#4](https://github.com/ccp-volume-em/vem-project-template/pull/4)).
- [ ] Try the `update-from-template` skill on a real project made from the
      template ([#11](https://github.com/ccp-volume-em/vem-project-template/pull/11)).
- [ ] Check for template updates on a schedule, as for the guide. This needs
      the template to be public (or a token), since a project's Actions can't
      read a private template ([#11](https://github.com/ccp-volume-em/vem-project-template/pull/11)).
- [ ] Review the docs tooling: Material for MkDocs reaches end of life in
      May 2027; its successor is [Zensical](https://zensical.org/).

## Open questions

- Questions that need a decision, with who decides.

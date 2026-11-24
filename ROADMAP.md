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
- [ ] Search for existing tools before building anything. Once the user
      has described what they want (e.g. in `start-project`'s *Purpose*
      question), search for tools that already do it, or nearly do it:
      napari hub, Fiji update sites, PyPI and conda-forge, the image.sc
      forum, BioImage Model Zoo and GitHub. Give the user a short report:
      - each option found (if any), what it does, and how well it fits;
      - how to use it: install and use as-is, contribute the missing part
        to the existing project, or fork and adapt (last resort);
      - roughly how much extra development each option needs;
      - anything else that matters: licence, whether it's maintained and
        still has active maintainers, community and documentation,
        compatible file formats, and how to cite it.

      Encourage reusing and contributing over reinventing the wheel: it
      saves effort and helps keep existing projects sustainable. Only
      write new code for what's left. Probably its own skill (e.g.
      `find-existing-tools`) that `start-project` calls and the user can
      also run before any new feature.

## Later

- [ ] A simpler starting point for Fiji-only projects, with no Python for the
      user to install: Groovy scripts and tests, expected results in CSV,
      and Python only inside GitHub's checks. Probably a second template
      (e.g. `vem-fiji-template`) synced from this one for shared files.
      Needs the Fiji tests running in CI first. Trade-off: no checks on the
      user's own computer before each commit, so it suits public
      repositories best.
- [ ] A lighter way to use the template's guidance, with no repository to
      set up: for a one-off standalone script or macro (e.g. a Fiji script
      to measure one dataset), the user points their AI assistant at the
      template and asks for the script. The assistant follows the same
      rules (Script Parameters, physical units, provenance, no hard-coded
      paths) and hands back a single file, with a short note on how to run
      and check it. It also reminds the user that a full GitHub repository
      (tests, version history, reviews, citation) is more sustainable once
      a script grows, gets reused or shared, or feeds into a paper, and
      offers to move it into one later. Probably a skill (e.g.
      `quick-script`) that works from a clone or from the template's GitHub
      page, plus a short section in `START_HERE.md` or the README.
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

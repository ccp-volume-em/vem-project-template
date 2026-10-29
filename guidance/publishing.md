# Making software public and releasing it

From the guide: [Making software public](https://ccp-volume-em.github.io/guide/software_publishing/).

A useful public release is installable, documented, licensed, citable, and
free of anything that should stay private.

## Before making a repository public

Review the **whole history**, not just the current files: deleting a secret
in the latest commit doesn't remove it from earlier ones.

- [ ] All contributors (and, where relevant, employers and funders) agree to
      release the software.
- [ ] No credentials, tokens, private URLs, personal or patient data,
      confidential discussions, or data you may not redistribute. Revoke and
      replace any credential that was ever committed.
- [ ] Licences of code, models, example data, fonts and icons checked;
      third-party copyright and attribution notices recorded.
- [ ] README, licence, install and usage instructions, contributing guide,
      citation file, and a way to report problems.
- [ ] Installed in a clean environment and tested, using the **built
      package**, not just the source checkout.
- [ ] Release version chosen and release notes written (important changes,
      known limitations, compatibility breaks).
- [ ] Before switching from private to public, inspect branches, tags, pull
      requests, Actions logs and release assets: they become visible too.

Don't commit large datasets, model weights or build output. Deposit large
research outputs in a public repository and link to them by persistent
identifier.

## Repository contents

`README.md` (purpose, status, platforms, install, minimal example, docs link,
support, citation), `LICENSE`, `CITATION.cff` (authors with ORCIDs, version,
date, DOI), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and an
accurate dependency/environment specification with supported language
versions.

Use an organisation-owned repository for collaborative projects. Give at
least two maintainers release permissions, and enable multi-factor
authentication and branch protection.

## Making a release

From a reviewed commit on the default branch:

1. Update the version, changelog, citation metadata and docs.
2. Run tests, and build docs and distributions in a clean environment.
3. Create an annotated tag, e.g. `v1.2.0`.
4. Create a GitHub Release from the tag, with release notes.
5. Publish packages and container images from the same tag, then test that
   users can install them with the documented commands.

Never move or reuse a published tag. If a release is faulty, publish a new
patch release and explain the problem.

Connect the repository to [Zenodo](https://help.zenodo.org/docs/github/) to
archive each release, and put the version DOI in `CITATION.cff`. Cite the
version DOI (not the concept DOI) when reproducibility needs an exact release.

## Licence

- Without a licence, others generally may not use, modify or share the code.
  See [Choose a License](https://choosealicense.com).
- Choose the licence before accepting outside contributions, with agreement
  of all copyright holders. Consider dependency licence compatibility,
  permissive vs. copyleft, employer/funder/ecosystem requirements, patents,
  attribution and commercial use.
- Common choices: BSD-3-Clause, MIT, Apache-2.0 (permissive); GPL-3.0
  (copyleft). Use an unmodified [OSI-approved licence](https://opensource.org/licenses)
  and its SPDX identifier in package metadata. Ask your institution's research
  software or legal team when unsure.
- Software, documentation, data and model weights may need separate licences;
  say which files each covers. Creative Commons suits docs and data, but
  [not software](https://choosealicense.com/non-software/).

## PyPI

- Follow the [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/);
  don't call `setup.py` directly.
- Put all build and package metadata in `pyproject.toml`: name, version,
  description, README, licence expression and files, required Python,
  dependencies, authors, project URLs, classifiers, optional dependencies.
- Build and check:

  ```bash
  python -m pip install --upgrade build twine
  python -m build
  python -m twine check --strict dist/*
  ```

- Inspect the archives and install the wheel in a fresh virtual environment.
  Compiled extensions need wheels for each supported OS, architecture and
  Python version.
- Try new packaging workflows on [TestPyPI](https://packaging.python.org/en/latest/guides/using-testpypi/)
  first. PyPI never lets you replace a published version.
- Automate releases with [Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
  instead of a stored token, restricted to protected tags or environments.
  Build once, test those exact files, and publish the same files.
- Afterwards, check the package page and test `pip install` and import.

## AI use

See [ai-use.md](ai-use.md) for AI-use statements in releases.

---
name: review-changes
description: Review the current branch against this project's standards and the CCP-volumeEM guidance before opening or updating a pull request, covering tests, docs, changelog, commit messages, data safety and AI acknowledgement. Use before opening a PR, or when asked to check, review or tidy a branch.
---

# Review a branch before opening a pull request

This review supports, and doesn't replace, review by a person. Report what
you find as a short checklist the user can act on, and fix only what they
agree to.

## 1. See what changed

```bash
git fetch origin
git log --oneline origin/main..HEAD
git diff origin/main...HEAD --stat
git diff origin/main...HEAD
```

## 2. Check

**Safety**
- [ ] No data, images, results, model weights or large files added.
- [ ] No passwords, tokens, keys, private URLs or personal data, in the diff
      or any commit on the branch.

**Correctness and tests**
- [ ] `pytest` passes; `ruff check .` and `ruff format --check .` are clean.
- [ ] New behaviour and bug fixes have tests whose expected values were worked
      out independently of the code. No test was weakened to make it pass.
- [ ] Code you (the AI) wrote has been read and understood by the user. Offer
      to walk them through anything non-trivial.

**Volume EM data handling** (where relevant)
- [ ] Large volumes are processed lazily or in chunks, never loaded whole
      without a reason.
- [ ] Voxel size, units, axis order and transforms are carried through to the
      output; measurements are in physical units.
- [ ] Outputs record provenance (software version, parameters, inputs).

**Documentation**
- [ ] Public functions have NumPy-style docstrings; comments explain *why*.
- [ ] User-facing changes are reflected in `README.md` / `docs/`.
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]`, in the right section,
      written for users. `ROADMAP.md` updated if relevant.

**History**
- [ ] Commit messages follow Conventional Commits, one logical change each.
- [ ] Commits substantially written with AI have an `Assisted-by:` trailer.
- [ ] *fixes / closes / resolves #N* appears only for issues this PR fully
      resolves.

**Versioning**
- [ ] The version in `pyproject.toml` is unchanged (it only changes in a
      release). Note whether this change would be a patch, minor or major
      release, and why, for the PR description.

## 3. Report and open the PR

List what passed, what needs fixing, and anything that needs a human
decision. Once fixed, push and open the PR with the template
(`.github/pull_request_template.md`), filling in every section, including AI
use. Don't merge it.

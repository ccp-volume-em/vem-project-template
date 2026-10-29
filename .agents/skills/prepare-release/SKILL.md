---
name: prepare-release
description: Prepare a new release - choose the SemVer level, update version, changelog and citation in a release pull request, then tag and publish once it is merged. Use only when a maintainer asks to make a release.
---

# Prepare a release

When to release is the maintainer's decision. Do this only when asked.

## 1. Check readiness

- `main` is up to date, CI passes on it, and there are no open PRs the
  maintainer wants included.
- `CHANGELOG.md` has entries under `[Unreleased]`. If it's empty, there's
  nothing to release.
- No placeholders remain (`git grep -n -i "Your Name\|you@example\|0000-0000-0000-0000"`).
- For a **first public** release, go through the checklist in
  `guidance/publishing.md` with the maintainer.

## 2. Choose the version

Read `[Unreleased]` and the merged PRs since the last tag
(`git log --oneline $(git describe --tags --abbrev=0 2>/dev/null)..HEAD`, or the
whole log if there's no tag yet). The release takes the **highest** level of
any change in it, using the rules in `AGENTS.md` → *Versions and releases*:

- **Patch** `x.y.Z`: only fixes, no change to the public surface.
- **Minor** `x.Y.0`: new features or options, deprecations, nothing breaks.
- **Major** `X.0.0`: something breaks for existing users. Before 1.0.0, use a
  minor bump and make sure the changelog marks it `**Breaking:**`.
- The first release is usually `0.1.0`.

Tell the maintainer which level you recommend and **why**, and agree it
before continuing. Don't default to minor.

## 3. Release pull request

**If this repository is the project template itself** (`gh repo view --json
isTemplate` says `true`), version only the template: skip steps 1, 2 and 5
below and leave `pyproject.toml` and `CITATION.cff` at `0.0.0`, because every
project made from the template copies them and starts unreleased. Only update
`CHANGELOG.md` (step 3) and the AI-use statement (step 4). The release
workflow recognises the template and publishes just the release notes.

On a branch `release-vX.Y.Z`:

1. `pyproject.toml`: set `version = "X.Y.Z"`.
2. `CITATION.cff`: set `version: "X.Y.Z"` and `date-released: "YYYY-MM-DD"`.
3. `CHANGELOG.md`: rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add
   a fresh empty `## [Unreleased]` above it, and update the comparison links at
   the bottom.
4. If AI use was substantive in this release, add an AI-use statement to the
   release notes (see `guidance/ai-use.md`). Ask the maintainer to confirm the
   wording.
5. Run `pytest`, and build and check the package:
   `python -m build && python -m twine check --strict dist/*`.
6. Commit as `chore(release): vX.Y.Z`, push, and open a PR. Stop: a person
   reviews and merges it.

## 4. After the release PR is merged

Only when the maintainer confirms the PR is merged:

```bash
git switch main && git pull
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
```

Pushing the tag runs `.github/workflows/release.yml`, which checks the tag
matches the version, builds and tests the package, and creates the GitHub
Release with the changelog section as notes. Watch it and report the result.

Never move, delete or reuse a published tag. If a release turns out to be
broken, make a new patch release that explains the problem.

## 5. Afterwards

- If Zenodo is connected, add the new version DOI to `CITATION.cff` and the
  README in a follow-up PR.
- If the project publishes to PyPI or a container registry, check that
  installing the new version works with the documented commands.

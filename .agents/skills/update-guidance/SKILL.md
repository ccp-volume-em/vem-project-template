---
name: update-guidance
description: Re-read the CCP-volumeEM good practice guide, find what changed since guidance/ was last updated, and update guidance/ and AGENTS.md to match. Use when asked to update or refresh the guidance, when the "guide has changed" issue is opened, or when the user asks whether the guidance is current.
---

# Update the CCP-volumeEM guidance

The files in `guidance/` are a distilled copy of the CCP-volumeEM guide
(<https://github.com/ccp-volume-em/guide>, published at
<https://ccp-volume-em.github.io/guide/>). `guidance/source.json` records the
guide commit they were written from, and which `guidance/` files each guide
page feeds into (`used_in`).

Explain each step to the user as you go. They may not know git well.

## 1. Find out what changed

Run, from the repository root:

```bash
python tools/check_guidance.py --diff
```

- Exit 0 means it's up to date. Tell the user, update `last_checked` in
  `guidance/source.json` only if they want that committed, and stop.
- Exit 2 means the check couldn't reach GitHub. If it mentions rate limits,
  set `GITHUB_TOKEN` (e.g. `export GITHUB_TOKEN=$(gh auth token)`) and retry.
  If you can't run commands, ask the user to run it, or read the guide's pages
  directly at the URLs above and compare them with `guidance/`.
- Exit 1 lists changed, new and removed guide pages, and the diff of each.

## 2. Read the current guide pages

For every changed or new page, read the **whole current page**, not just the
diff, so you understand the context:
`https://raw.githubusercontent.com/ccp-volume-em/guide/main/<path>`.
Also check `mkdocs.yml` in the guide for pages that were added to or removed
from the navigation.

## 3. Summarise for the user before editing

Tell the user, in plain language:

- what changed in the guide (new advice, changed advice, removed advice);
- which `guidance/` files and which parts of `AGENTS.md` that affects;
- anything that conflicts with this project's *Project-specific notes* in
  `AGENTS.md`, or with code already in the repository.

Ask before going ahead if any change is large or conflicts with the project.

## 4. Update the files on a branch

1. Create a branch from the latest `main`: `update-guidance-<YYYY-MM-DD>`.
2. Edit the affected `guidance/*.md` files. Keep their style: short,
   checklist-like, imperative bullet points, each page linking to its guide
   source. Say only what the guide says: don't add advice of your own, and
   don't drop advice that's still in the guide.
3. For a **new** guide page, either fold it into the most relevant existing
   page or create a new `guidance/<topic>.md`, and add it to the table in
   `guidance/README.md` and the *Guidance* table in `AGENTS.md`.
4. For a **removed** page, remove or rewrite the advice that came only from it.
5. If a change affects a rule in `AGENTS.md` (e.g. testing, versioning, data
   handling, AI use), update that rule too. Never touch the
   *About this project* or *Project-specific notes* sections.
6. Update `guidance/source.json`: set `commit` and `commit_date` to the latest
   guide commit, `last_checked` to today, each page's `sha` to its current
   blob hash, and `used_in` for any new or renamed pages. Get the hashes from:
   `https://api.github.com/repos/ccp-volume-em/guide/git/trees/main?recursive=1`
   (or `gh api "repos/ccp-volume-em/guide/git/trees/main?recursive=1"`).
7. Run `python tools/check_guidance.py`: it should now report *up to date*.

## 5. Commit and open a pull request

- Commit with a message like
  `docs(guidance): update to guide commit <short-sha>`, with a body listing the
  main changes and an `Assisted-by:` trailer.
- Add a `Development` entry to `CHANGELOG.md` under `[Unreleased]`.
- Push and open a PR that summarises what changed in the guide and how the
  guidance was updated, linking the guide's commit comparison:
  `https://github.com/ccp-volume-em/guide/compare/<old-sha>...<new-sha>`.
- If a "guide has changed" issue is open, write "Fixes #N" in the PR.
- Stop there: a person reviews and merges the PR.

## 6. Suggest follow-up work

If the new guidance means the **code** should change (e.g. a new testing or
metadata recommendation), don't change code in this PR. List the follow-ups
for the user and offer to open issues for them.

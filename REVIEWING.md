# Reviewing a pull request

A review is a second look at a change before it becomes part of `main`. It's
the main way this project catches mistakes, especially in code an AI
assistant wrote, which can look convincing and still be wrong.

Use this page whether you're reviewing a colleague's pull request (PR) or
your own. You don't need to be a programmer to review well: most of what
matters is whether the change does the right thing *scientifically*, and
whether you can see the evidence that it does.

- [Reviewing someone else's PR](#reviewing-someone-elses-pr)
- [Reviewing your own PR](#reviewing-your-own-pr), if you work alone
- [Using GitHub's review tools](#using-githubs-review-tools)

## Reviewing someone else's PR

### 1. Understand what it's for

Read the PR description and the issue it links to. Before looking at any
code, you should be able to say what the change is meant to do and why. If
you can't, ask the author: that's a useful review comment in itself.

### 2. Check the science

This is where a reviewer adds most, and it's the part an AI can't do for the
author.

- **Is the method right** for this data? Are thresholds, parameters and
  defaults sensible, and are they the author's choices rather than an AI's
  defaults? Choices like these should be explained in the PR.
- **Are the results believable?** Ask for, or run, a small example whose
  answer you can work out by hand. For volume EM, check **physical units**,
  **anisotropic voxels** (e.g. 8 nm in-plane, 16 nm between slices) and
  **axis order** (z, y, x): these are the commonest silent errors.
- **Is the metadata kept?** Voxel size, units and transforms should reach the
  output, and outputs should record how they were made (`provenance.json`).

### 3. Check the tests

- New behaviour and bug fixes have tests.
- The expected values were **worked out independently**, not copied from what
  the code produced. Ask the author how they got them.
- No test was deleted, loosened or skipped to make the checks pass.
- If you're unsure the tests would catch a mistake, ask the author to break
  the code on purpose (e.g. drop the voxel size) and show a test fails.

### 4. Look out for AI-specific problems

AI-written code tends to fail in recognisable ways. Look for:

- **Confident but wrong:** code that runs and looks tidy, but answers a
  slightly different question from the one asked.
- **Invented details:** functions, options or file-format fields that don't
  exist, or citations and links that go nowhere.
- **Silent workarounds:** errors caught and ignored, values clipped, or edge
  cases skipped without saying so.
- **More than was asked:** extra features, rewritten files or "tidying" that
  makes the change hard to check. Ask for it to be split up.
- **Copied code:** large blocks that look lifted from elsewhere may carry a
  licence that needs crediting.

### 5. Check the basics

- **Safety:** no data, images, results, passwords or personal information
  added, in any file or commit.
- **Scope:** the PR changes only what it says it does.
- **Records:** `CHANGELOG.md` has an entry (except for automated dependency
  updates); docs and docstrings match what the code now does; the PR says how
  AI was used.
- **Checks:** there's a green tick ✅ on the PR. If there's a red cross ❌, find
  out why before approving.

The `review-changes` skill checks the project standards (changelog, commit
messages, docs). Ask the author to run it, or run it yourself, so you can
spend your time on the science.

### 6. Give useful feedback

- **Be specific:** point at the line, say what concerns you, and why.
- **Ask, don't assume:** "How did you get 1,024 here?" works better than
  "this is wrong".
- **Say what matters:** make clear which comments must be fixed before
  merging and which are suggestions (many reviewers start minor ones with
  "optional:" or "nit:").
- **Say what's good,** too. Reviews are for learning as well as checking.

### 7. Decide

- **Approve** when you understand the change, the evidence convinces you,
  and the checks pass. Then merge it, or tell the author it's ready.
- **Request changes** when something must be fixed first, and say what.
- **Comment** when you have questions but no verdict yet.

It's fine to approve a change you didn't fully follow if a part is outside
your expertise, as long as you say so in your review, so someone else can
check that part.

## Reviewing your own PR

Many projects have one developer, so a second reviewer isn't required. If
there's no one to ask, review the PR yourself, then merge it. For changes that
alter scientific results, delete data, or go into a release, try to find a
second person anyway, even occasionally: a colleague's half hour, or a
question on [image.sc](https://forum.image.sc/).

The risk in self-review, especially of AI-written code, is reading the summary
and agreeing with it. Treat the change as if someone you don't know wrote it:

1. **Wait first.** Review after a break (the next day if you can), not
   straight after writing it. Open it as a *draft* PR until you have.
2. **Read the diff, not the summary.** Use the PR's *Files changed* tab and
   read every line. Tick *Viewed* on each file as you go.
3. **Explain it back.** Without looking at the AI's description, write two or
   three sentences on what the change does and why. If you can't, it isn't
   ready: ask the AI to explain the parts you can't.
4. **Check the evidence yourself.** Look at the test results on the PR rather
   than taking "tests pass" on trust. Run it on a small example whose answer
   you worked out by hand.
5. **Test the tests.** Were the expected values worked out independently of
   the code? Ask the AI to break the code on purpose (e.g. swap two axes,
   drop the voxel size) and check that a test fails.
6. **Look for what's missing,** not just what's there: empty or single-slice
   input, anisotropic voxels, units, unexpected data types, error messages a
   user would understand.
7. **Check the scope.** The diff contains only what you meant to change: no
   unrelated edits, no deleted or weakened tests, no data or secrets.
8. **Ask for an independent second opinion.** Start a *fresh* AI session that
   hasn't seen the work, show it the diff, and ask "what could make this
   wrong?" rather than "is this OK?". Treat what it finds as leads to check,
   not verdicts.
9. **Leave a note.** Add a PR comment saying what you checked and how. It's
   the record a reviewer would have left, and it helps future you.

The `review-changes` skill checks the project standards (changelog, commit
messages, docs) for you, but the judgement in steps 3–6 is yours.

## Using GitHub's review tools

On the PR's page on GitHub:

1. Open the **Files changed** tab to see every line that changed: red lines
   were removed, green lines were added. Tick **Viewed** on each file as you
   finish it.
2. To comment on a line, hover over it and click the blue **+** that appears.
   Write your comment and click **Start a review**, so your comments are sent
   together rather than one by one.
3. When you've finished, click **Review changes** (top right), write a short
   summary, choose **Comment**, **Approve** or **Request changes**, and click
   **Submit review**.
4. If you approved and you're the one merging, go back to the **Conversation**
   tab and click **Merge pull request**. GitHub then deletes the branch
   automatically if the repository is set up to.

GitHub doesn't let you approve your own PR. When you review your own work,
leave your notes as a comment instead (step 9 above), then merge.

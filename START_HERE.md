# Start here

**For researchers who are new to coding or GitHub.** You don't need to know how
to program to use this project. An AI assistant writes and runs the code. You
decide what it should do, check the results, and stay in charge of the science.

This page covers everything you need to get going. Read it once, then keep it
open while you work.

---

## What is this?

This is a ready-made starting point for writing analysis code for volume EM
and CLEM data. Good habits are built in: your work is saved step by step,
every change is checked by another person before it counts, and tests run
automatically to catch mistakes.

It lives on **GitHub**, a website that stores code and keeps its full history,
much like a lab notebook that never loses a page.

## What you need

- **A GitHub account.** Free at [github.com](https://github.com). Ask your group
  leader or the project maintainer to add you to your organisation on GitHub.
- **An AI coding assistant** that can work with files, not just chat. Examples
  include Claude Code, GitHub Copilot, Cursor and Codex. Some run in your web
  browser and connect to GitHub directly, so there's nothing to install;
  others run on your own computer. Check which ones your institute approves.
- **Ideally, someone to check your changes:** a colleague, supervisor or the
  project maintainer. If you work alone, you'll check them yourself, using
  [*Before you merge*](#before-you-merge) below.

## Seven words you'll hear

Your AI assistant will use these words. You don't need to remember the
details, only the idea.

| Word | What it means |
| --- | --- |
| **repository** (or "repo") | The project: all its files and their full history, stored on GitHub. |
| **commit** | A saved step, with a short note saying what changed and why. Like a dated entry in a lab notebook. |
| **branch** | A separate working copy for one piece of work, so the main version isn't affected while you try things. |
| **`main`** | The main, checked version of the project that everyone relies on. |
| **pull request** (or "PR") | A request to add the work on a branch into `main`. It shows exactly what changed, and it's where someone reviews it. |
| **review** and **merge** | Another person reads the pull request and approves it. "Merging" adds it to `main`. |
| **issue** | A note on GitHub describing a task, an idea or a problem. Like a to-do list everyone can see. |

You'll also see **tests** (small automatic checks that the code gives the right
answers) and a **green tick ✅ or red cross ❌** next to each pull request,
showing whether those checks passed.

## How a change happens

Every change, big or small, follows the same five steps. Your AI assistant does
the technical parts; you make the decisions.

1. **You describe** what you want, in your own words.
2. **The AI suggests a plan.** You agree to it, or ask questions first.
3. **The AI makes the change** on a branch, runs the tests, and saves commits.
4. **The AI opens a pull request.** You read the changes, try them out, and,
   if you can, ask a colleague to review it.
5. **Your reviewer (or you, after checking it yourself) merges it.** Now it's
   part of `main`, and
   the AI deletes the branch: its work is safe in `main`, and this keeps the
   project tidy.

Nothing reaches `main` without a person checking it, even if that person is
you. The AI never merges its own work.

## Your first session

1. **Make your own copy of this template.** On this project's GitHub page,
   click the green **Use this template** button, then **Create a new
   repository**. Give it a short name (e.g. `mito-volume-analysis`), choose
   **Private**, and click **Create repository**. If you can't see the button,
   ask the maintainer to give you access.
2. **Open your new repository in your AI assistant.** How depends on the tool:
   browser-based assistants let you pick the repository from a list; on your
   own computer, ask the assistant to "download (clone) my repository
   *name* from GitHub".
3. **Say:**
   > I'm new to coding and GitHub. Please read `AGENTS.md` and `START_HERE.md`,
   > then run the start-project skill. Explain each step in plain language.
4. **Answer its questions.** It asks what the project is for, who's involved
   and a few choices. If you're unsure, say so and ask it to explain the
   options.
5. **It opens your first pull request.** Ask your reviewer to look at it, or
   check it yourself (see *Before you merge*). Once it's merged, your project
   is ready.

## Things you can say

You don't need special commands. Talk to the assistant as you would to a
helpful colleague. Some examples:

| You want to… | Try saying… |
| --- | --- |
| Start something new | "I'd like to measure the surface area of each mitochondrion in my segmentation. Before writing anything, can you suggest how, and what could go wrong?" |
| Understand code | "Explain what `measure.py` does, in plain words, without jargon." |
| Check it works | "Run the tests and tell me what they check." |
| Check it on real data | "Run it on the example data and show me the results. How can I check one value by hand?" |
| Save your progress | "Commit what we've done so far, with a clear message." |
| Get it reviewed | "Open a pull request for this, and summarise it for my reviewer." |
| Review it yourself | "I'm reviewing this alone. Walk me through the changes file by file, and tell me what could make it wrong." |
| See what's changed | "What has changed in the project since last week?" |
| Get unstuck | "Stop. Explain what went wrong, and don't change anything yet." |
| Plan ahead | "Make an issue for adding a 3D view, so we don't forget." |
| Work in Fiji | "Make a Fiji script that measures the volume of each object in my label image." (It's written so Fiji shows a dialog for the settings.) |
| Tidy up | "The pull request was merged. Please tidy up the branch." |

## Before you merge

Check these yourself, whether or not someone else reviews it. A reviewer will
ask about them too.

- [ ] **I understand what the change does.** If not, ask the AI to explain
      until you do. You're responsible for it, not the AI.
- [ ] **It gives the right answer on something I can check.** For example,
      a small example where you can work out the answer by hand.
- [ ] **The tests are right.** Ask the AI what each new test checks, and
      whether *you* agree the expected numbers are correct. An AI can write a
      test that agrees with its own mistake.
- [ ] **The checks passed** (green tick ✅ on the pull request).
- [ ] **No data, images, passwords or personal information** were added.

**Working alone?** The danger is reading the AI's summary and agreeing with
it. A few habits help:

- **Come back to it later,** ideally the next day, before merging.
- **Read the changes, not the summary:** the *Files changed* tab on the pull
  request shows every line.
- **Explain it in your own words** before you merge. If you can't, ask the AI
  until you can.
- **Ask the AI to break it on purpose,** and check that a test catches it.
- **Ask a fresh AI session** (one that didn't write it) "what could make this
  wrong?", and check what it says yourself.
- **For anything that changes your results,** try to get a colleague to look,
  even briefly.

The full checklist is in [REVIEWING.md](REVIEWING.md#reviewing-your-own-pr).

## Golden rules

1. **Data never goes on GitHub.** Keep images and results on your institute's
   storage. The project is set up to ignore them, but stay alert.
2. **Don't paste unpublished data, patient data or passwords into an AI tool**
   unless your institute has approved that tool for such data.
3. **Every change is reviewed before it's merged,** by a colleague if
   possible, otherwise carefully by you. The AI never merges.
4. **Scientific decisions are yours.** Thresholds, methods and parameters
   should be your choice, not the AI's default. Ask it for the options and
   their trade-offs.
5. **When unsure, stop and ask** a person.

## When to stop and ask a person

Ask your reviewer or the maintainer, rather than letting the AI decide, if:

- the AI wants to **delete** files, **discard** work, or do anything it calls
  "force" or "reset";
- a check fails (red cross ❌) and the AI suggests changing the **tests** to
  make it pass;
- you're asked about **licences**, **making the project public**, or
  **publishing** a release;
- results look **surprising**, or you can't explain them.

## If something goes wrong

Don't worry: GitHub keeps every saved step, so earlier work can almost always be
recovered. Tell your assistant:

> Stop. Explain what happened in plain words, and don't change anything yet.

Then decide together what to do, and ask a person if you're unsure.

## Where next

- **[CONTRIBUTING.md](CONTRIBUTING.md):** the detailed reference for how work
  flows. Useful as you get more confident. Your AI assistant follows it for you.
- **[guidance/](guidance/README.md):** good practice from the CCP-volumeEM
  community, for example on file formats and testing.
- **Help:** ask the project maintainer, or the
  [image.sc forum](https://forum.image.sc/) for image analysis questions.
- **Learning more:** the Software Carpentry lesson on
  [version control with git](https://swcarpentry.github.io/git-novice/)
  explains the ideas above in more depth.

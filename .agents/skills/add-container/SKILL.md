---
name: add-container
description: Add a container image (a Dockerfile, a GitHub Actions check that it builds and starts, and optional publishing on release) to a project that left it out at setup, using the template's version adapted to the project. Use when the user wants to containerise the tool, run it with Docker or Apptainer (e.g. on an HPC cluster), or asks to "add Docker" or "add a container".
---

# Add a container

A container packages the tool with the exact versions of everything it needs,
so it runs the same on a laptop, an HPC cluster or a colleague's computer.
The template has one, but projects can leave it out at setup. This skill puts
it back, adapted to the project. Read `guidance/containers.md` first.

## 1. Ask

- **Why?** Running on an HPC cluster (Apptainer), sharing with people who
  shouldn't have to install Python, or re-running a published analysis
  exactly. The answer decides whether to publish images (below).
- **Is there a Python tool to package?** The template's container runs the
  project's command-line tool. For a Fiji-only project, explain that this
  container doesn't fit, and ask a maintainer before going further.
- **GPU?** If the code uses a GPU, the image needs a CUDA base image instead
  of the slim Python one (`guidance/containers.md`).

## 2. Copy the template's files

Work on a branch (e.g. `add-container`). Take the files from the template
version the project is based on, so they match its other shared files;
`update-from-template` brings later changes. `.github/template.json` gives
the template `repository` and `commit` (if it's missing, run
`python tools/check_template.py --init` first).

```bash
base=https://raw.githubusercontent.com/<repository>/<commit>
curl -fsSL "$base/Dockerfile" -o Dockerfile
curl -fsSL "$base/.dockerignore" -o .dockerignore
curl -fsSL "$base/.github/workflows/container.yml" -o .github/workflows/container.yml
```

For a private template, add `-H "Authorization: Bearer $(gh auth token)"`.

## 3. Adapt them to the project

- **`Dockerfile`:** replace the template's example names (`vem-project`) in
  the comments, the `LABEL`s (title, description, source repository,
  licence) and `ENTRYPOINT`, which must be the project's command from
  `[project.scripts]` in `pyproject.toml`. If the project has no command,
  ask what the container should run (e.g. `python -m <package>`), and
  change the `--version` and `--help` checks in `container.yml` to match.
- **`.github/dependabot.yml`:** add the entry that keeps the base image up to
  date:

  ```yaml
    - package-ecosystem: docker
      directory: /
      schedule:
        interval: monthly
      commit-message:
        prefix: build
  ```

- **Documentation:** add `Dockerfile             container image` to the
  folder tree in `README.md`. If the project has a documentation site, copy
  the *Container* section of the template's `docs/usage.md` (from the same
  commit) into the project's, adapted, and mention the container in
  `docs/index.md`. Otherwise add a short *Container* section to the README.
- **`AGENTS.md`:** remove the "No container" line from *Project-specific
  notes*.
- **`CHANGELOG.md`:** an `Added` entry, e.g. "A container image, to run the
  tool with Docker or Apptainer". A new way to run the tool is a minor
  release.

## 4. Check it

If Docker is installed, build and start it, and explain each step:

```bash
docker build -t <name> .
docker run --rm <name> --version
```

Otherwise explain that the *Container* check on the pull request builds and
starts the image on GitHub. Either way, open the PR and let the checks run.

## 5. Publishing (optional)

The *Container* workflow can publish the image to the GitHub Container
Registry on each release, so others can `docker pull` or `apptainer pull` it
without building it. It's off until the repository variable
`PUBLISH_CONTAINER` is `true` (Settings → Secrets and variables → Actions →
Variables). That's a repository setting: explain it and let the user decide,
or set it with their agreement (`gh variable set PUBLISH_CONTAINER --body true`).

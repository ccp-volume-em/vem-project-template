---
name: find-existing-tools
description: Search for existing tools (napari plugins, Fiji plugins and update sites, Python packages, pretrained models) that already do what the user wants, or nearly do, and give them a short report of the options before any new code is written. Use when a project starts (start-project calls it), before building a new feature or script, or when the user asks "does something already do this?".
---

# Find existing tools before building

Before writing new code, check whether someone has already written it. Using
or improving an existing tool usually saves a lot of work, gives the user
something already tested by others, and helps keep that project alive.
Writing a new tool is the last option, for what nothing else covers.

## 1. Understand what's needed

Make sure you can say, in one or two sentences, what the user wants to do:
the task (e.g. segment mitochondria, register light microscopy to EM,
measure object volumes), the kind of data (FIB-SEM, SBF-SEM, array
tomography, CLEM; 2D or 3D; rough size; file format), and how they want to
run it (Fiji, napari, Python, command line, HPC). If any of that is unclear,
ask.

Search with a general description of the task only. Never put unpublished
data, images, sample details or anything confidential into a search
(`AGENTS.md`, *Volume EM and CLEM data*).

## 2. Search

Look in the places volume EM and CLEM tools are shared, starting with those
that fit how the user wants to work:

- **Fiji:** the [list of update sites](https://imagej.net/list-of-update-sites/)
  and [imagej.net](https://imagej.net/) plugin pages, and what Fiji does
  already (e.g. *Analyze › 3D Objects Counter*, MorphoLibJ);
- **napari:** the [napari hub](https://napari-hub.org/);
- **Python:** [PyPI](https://pypi.org/), [conda-forge](https://conda-forge.org/)
  and well-known libraries (scikit-image, SciPy, dask, ome-zarr-py);
- **models:** the [BioImage Model Zoo](https://bioimage.io/) for pretrained
  deep-learning models;
- **the community:** the [image.sc forum](https://forum.image.sc/) (people
  often ask the same question there), the
  [CCP-volumeEM guide](https://ccp-volume-em.github.io/guide/), and GitHub.

If you can't search the web, say so, and tell the user where to look
instead. Don't list tools from memory as if you had checked them: say which
ones you know of but couldn't check.

For each promising tool, look at its documentation and repository: what it
does, whether it handles the user's kind of data, when it was last released
or changed, whether issues get answers, and its licence.

## 3. Report

Give the user a short report, in plain language: a sentence or two per
option, not a long list. Leave out tools that clearly don't fit. If you found
nothing suitable, say so, and what you searched.

For each option:

- **What it is and how well it fits:** what it does, and what the user needs
  that it doesn't do.
- **How to use it**, one of:
  - **Use it as it is:** install it and use it, perhaps with a small script
    around it. The least work.
  - **Contribute to it:** add the missing part to the existing project, by
    opening an issue to ask the maintainers first, then a pull request. A
    little more work, but everyone gets the improvement, and the project
    stays maintained.
  - **Fork and adapt it:** make your own copy and change it. Only when the
    project is no longer maintained, or the maintainers don't want the
    change: a fork is yours to maintain from then on.
- **How much extra development:** none, a little (a script or a few
  settings), some (a new feature in someone else's code), or a lot.
- **Anything else that matters:** whether it's still maintained, its licence
  (and whether it fits the user's plans), documentation and help, file formats
  it reads and writes (OME-Zarr, TIFF, N5), whether it handles volumes too big
  for memory, and how to cite it.

End with your recommendation and why. Explain that reusing and contributing
to existing tools, rather than reinventing them, saves effort and helps keep
those projects sustainable: their maintainers rely on people using, citing
and improving their work. Then let the user choose.

## 4. Afterwards

- **If an existing tool does the whole job,** the user may not need new code
  at all. Say so plainly. Offer to help them install and try it, and remind
  them to cite it.
- **If they'll contribute to a tool,** help them write a clear issue for
  that project first. Follow that project's own contributing guide, not this
  template's.
- **If they'll build something new,** or a small part on top of an existing
  tool, carry on with what they asked for, building only what's missing.
- **In a project made from this template,** offer to record the choice in
  `docs/decisions.md`: which tools were considered, which was chosen and why.
  If they'll use a tool from their code, it becomes a dependency: ask before
  adding it to `pyproject.toml`.

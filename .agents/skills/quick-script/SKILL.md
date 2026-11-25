---
name: quick-script
description: Write a single standalone script or macro (Fiji, Python) for a one-off job, following the template's good practice, without setting up a repository. Use when the user wants "just a script" for one dataset or a quick task and doesn't have, or want, a project made from the template. Reminds them a full GitHub repository is more sustainable for larger or longer-lived work.
---

# Write a one-off script

The user wants one script for a small, one-off job (e.g. measure the objects
in one segmentation, convert a folder of TIFFs to OME-Zarr), not a whole
project. Give them a single file that follows the same good practice as a
project made from this template, with nothing to set up.

The user may be reading this from the template's GitHub page rather than a
copy of it. The rules it points to are in the template's
[`AGENTS.md`](../../../AGENTS.md) and [`guidance/`](../../../guidance/README.md):
read them from the same place you read this file (e.g.
`https://github.com/ccp-volume-em/vem-project-template`). Don't create or
change anything in the template itself.

If the user is already working in a project made from the template, this
skill isn't needed: write the code in the project as usual (for Fiji, with
the `new-fiji-script` skill).

## 1. Agree what it does

As in `new-fiji-script`, confirm in plain language:

- the input (file type, 2D or 3D, how big) and the output;
- every setting they'll want to change, with sensible defaults;
- any scientific choice (method, threshold): theirs to make, not yours;
- where it will run: Fiji, Python on their computer, or a cluster.

Then run the `find-existing-tools` skill, briefly: if Fiji, napari or a
package already does this, they may not need a script at all, or only a few
lines around an existing tool.

## 2. Write it

Follow `AGENTS.md`, *Fiji scripts* and *Volume EM and CLEM data*, which
apply to a single file just as to a project:

- **Fiji:** Script Parameters (`#@` lines) for every input, never a
  hand-built dialog (`GenericDialog`, or `Dialog.create` in a macro), in any
  language. Groovy, unless the user asks for another: if they say "macro",
  ask whether they need the ImageJ macro language itself. Script Parameters
  work in ImageJ macros too (see `new-fiji-script` for how).
- **Python:** one `.py` file. Take settings on the command line
  (`argparse`), with defaults. List the packages it needs, with versions, in
  an [inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/)
  block at the top, so `uv run script.py` or `pipx run script.py` installs
  them, and say how to install them with pip instead.
- **Either way:** a header comment saying what it does, its inputs and
  outputs, and how to run it; no hard-coded paths; results in physical units,
  with a clear stop if the voxel size is missing; large volumes read lazily
  or slice by slice; and a `provenance.json` (or a few provenance lines in
  the output) with the settings, inputs, software versions, date and the
  script's checksum.

Keep it short and readable: the user should be able to follow it.

## 3. Check it

- If you can run it, run it on a small synthetic image whose answer can be
  worked out by hand, and show the user the result next to the expected
  answer.
- Either way, give the user one simple check they can do themselves (e.g.
  "this box is 100 × 100 × 50 voxels of 10 × 10 × 20 nm, so 1 µm on each
  side, and its volume should be 1 µm³"), and ask them to run it once on their data and look at the
  output before trusting it.

## 4. Hand it over

- Save it where the user asks, outside the template, or give it to them as a
  file to download. Explain how to run it and what each setting does.
- Suggest they note in their lab notebook (or methods) which script and
  settings produced which results, and keep the script with the
  `provenance.json`.

## 5. Remind them about a repository

End with a short, friendly reminder, in your own words:

> This script is fine for a one-off job. If it grows, you run it again on
> new data, other people use it, or its results go into a paper, a full
> GitHub repository made from the CCP-volumeEM template is more
> sustainable: it keeps the full history, has tests that check the answers,
> gets each change reviewed, and can be cited. Your script can move into
> one later. Just ask.

If they want to move it later, point them to `START_HERE.md`: once the
project is set up, the script goes in `fiji/` (via `new-fiji-script`) or
`src/`, with tests.

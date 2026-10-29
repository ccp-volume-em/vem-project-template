---
name: new-fiji-script
description: Create a new Fiji script as a Groovy script with Script Parameters (#@) for its dialog, so it runs both in the Fiji GUI and headless, with a test. Use for any Fiji or ImageJ work unless the user asks for a different language (e.g. an ImageJ macro, Jython or a Java plugin).
---

# Create a Fiji script

Fiji work in this project is written as **Groovy scripts with Script
Parameters**, unless the user asks for something else. Script Parameters are
`#@` lines at the top of the script. Fiji builds the dialog from them, records
them for reproducibility, and accepts them on the command line for headless and
HPC runs. Use `fiji/measure_object_volumes.groovy` as the model.

## 1. Agree what it does

Before writing, confirm with the user, in plain language:

- the input (file type, 2D or 3D, label image or intensities, how big);
- every parameter they'll want to change, with sensible defaults and ranges;
- the outputs (tables, images) and where they go;
- any scientific choice (method, threshold): theirs to make, not yours.

## 2. Write `fiji/<verb>_<thing>.groovy`

Follow the rules in `AGENTS.md` → *Fiji scripts*. In order:

1. **Script Parameters first**, one per input, each with a `label`, a `value`
   (default) where sensible, `min`/`max` for numbers, `style` for files and
   folders (`"file"`, `"directory"`, `"save"`), and `description` for anything
   that needs explaining. Add `#@ LogService log` for messages and
   `#@output` for values worth returning. Examples:

   ```groovy
   #@ File (label = "Input image", style = "file") inputFile
   #@ File (label = "Output folder", style = "directory") outputDir
   #@ Double (label = "Minimum volume (µm³)", value = 0.1, min = 0) minVolume
   #@ String (label = "Method", choices = {"Otsu", "Li", "Triangle"}) method
   #@ Boolean (label = "Save QC images", value = true) saveQc
   #@ LogService log
   ```

2. **A header comment** saying what the script does, its inputs and outputs,
   and how to run it.
3. **The work**, with comments explaining *why*. Use explicit getters
   (`imp.getStack()`, `cal.getUnit()`): Groovy's property shortcuts can pick
   the wrong method (`imp.stack` is `isStack()`).
4. **Outputs plus a `provenance.json`** with the parameters, input paths,
   `IJ.getFullVersion()`, the date and the script's SHA-256 checksum (the
   script's path is `binding.variables["javax.script.filename"]`).

## 3. Test it

1. Add tests to `tests/test_fiji_scripts.py`, marked `@pytest.mark.fiji`, that
   run the script on a small synthetic image (made with `tifffile`, with
   `metadata={"axes": "ZYX"}` and a voxel size) and compare the output with
   values worked out by hand. Test what happens with bad input too.
2. Run them: `FIJI=/path/to/Fiji.app/fiji pytest -m fiji`. Find the Fiji
   launcher first (on macOS usually `/Applications/Fiji.app/fiji`); if there's
   no Fiji, say so and ask the user to run the tests.
3. Ask the user to open it in Fiji and click **Run** once, to check the
   dialog reads well.

## 4. Document and commit

- Add the script to the table in `fiji/README.md`. If the project has no
  `fiji/` folder yet, create it, copying `fiji/README.md` from the project
  template and replacing its example rows, and add the *Fiji scripts* section
  back to `CONTRIBUTING.md` from the template.
- Add a `CHANGELOG.md` entry under `[Unreleased]` → `Added`.
- Commit (`feat(fiji): add <script name>`) and open a pull request as usual.

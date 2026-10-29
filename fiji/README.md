# Fiji scripts

Scripts for [Fiji](https://fiji.sc), written in Groovy. Each script declares
its inputs as **Script Parameters** (the `#@` lines at the top). Fiji turns
these into a dialog automatically when you run the script, and the same script
also runs without a screen, e.g. as a batch job on an HPC cluster.

| Script | What it does |
| --- | --- |
| [`measure_object_volumes.groovy`](measure_object_volumes.groovy) | Physical volume of each object in a 3D label image, with a provenance record |

## Try it

Make a small test volume (needs `tifffile`: `python -m pip install tifffile`):

```bash
python examples/make_example_data.py
```

Then run `measure_object_volumes.groovy` (below) on `data/example_labels.tif`.
Object 1 should measure 3,276,800 nm³ and object 2 19,660,800 nm³, the same
as the Python tool gives for the OME-Zarr version.

## Run a script in Fiji

1. Drag the `.groovy` file onto the Fiji window, or use **File > Open**. It
   opens in the script editor.
2. Click **Run**. A dialog asks for the parameters.
3. Results and a `provenance.json` record are written to the output folder you
   chose. Messages appear in the Console window.

To add a script to Fiji's menus, copy it into `Fiji.app/scripts/Plugins/` and
restart Fiji.

## Run a script without the GUI (headless)

Give every parameter on the command line, as `name="value"` pairs separated by
commas:

```bash
/path/to/Fiji.app/fiji --headless --run fiji/measure_object_volumes.groovy \
    'labelFile="/data/labels.tif",outputDir="/data/results",requireCalibration=true'
```

If Fiji replies `Macro or script not found: …/--run`, your Fiji's launcher
needs the main class named explicitly:

```bash
/path/to/Fiji.app/fiji --headless --main-class=net.imagej.Main -- \
    --headless --run fiji/measure_object_volumes.groovy \
    'labelFile="/data/labels.tif",outputDir="/data/results",requireCalibration=true'
```

On older Fiji installations the launcher is called `ImageJ-linux64`,
`ImageJ-win64.exe` or `Contents/MacOS/ImageJ-macosx` instead of `fiji`.

Fiji exits normally even when a script fails, so check the output for
`[ERROR]` lines and that the expected files were written.

## Test the scripts

The tests in `tests/test_fiji_scripts.py` check every script uses Script
Parameters. To also run the scripts on small test images, point `FIJI` at your
Fiji launcher:

```bash
FIJI=/Applications/Fiji.app/fiji pytest -m fiji
```

These tests don't run in GitHub Actions, which has no Fiji, so run them
locally before opening a pull request that changes a script.

## Writing a new script

Ask your AI assistant to use the **new-fiji-script** skill, or follow
`.agents/skills/new-fiji-script/SKILL.md`. The rules are in `AGENTS.md` →
*Fiji scripts*.

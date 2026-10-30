# Notebooks

Jupyter notebooks for **this project's own analysis**: exploring your data,
trying parameters, and making figures. They use the code in `src/`; they
don't replace it.

| Notebook | What it does |
| --- | --- |
| [`example_measure.ipynb`](example_measure.ipynb) | Measures the example volume and plots the object volumes |

## Run them

```bash
python -m pip install -e ".[notebooks]"
jupyter lab
```

## Good habits

- **Parameters at the top.** Put paths and settings in the first code cell,
  so it's clear what to change, and never hard-code paths to your own
  computer further down.
- **Run top to bottom before committing:** *Kernel → Restart Kernel and Run
  All Cells*. A notebook that only works when cells are run in a particular
  order can't be reproduced.
- **Outputs aren't saved in git.** Plots and tables in notebooks can be large
  and may show unpublished data, so a pre-commit hook (nbstripout) removes
  them when you commit, and a test checks none slip through. Save figures you
  want to keep to `results/`.
- **Move reusable code into `src/`.** Once a function is used in more than one
  notebook, or other people will run it, move it into the package with a
  docstring and a test, and import it.
- **Record decisions.** If a notebook leads you to choose a threshold or
  method, add it to [`docs/decisions.md`](../docs/decisions.md).
- **No data in notebooks:** read it from `data/` or your institute's storage.

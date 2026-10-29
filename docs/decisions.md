# Decisions

The scientific and analysis choices made in this project, and why: methods,
thresholds, parameters and their defaults, what is excluded, and how results
are reported. Code shows *what* was done; this page records *why*, so the
reasoning survives for reviewers, for the methods section of a paper, and for
whoever works on the project next.

**When to add an entry:** whenever a choice could change the results. Add it
in the same pull request as the change. Newest first. Don't edit old entries
when you change your mind: add a new one that replaces them, and say so.

**How:** copy the template below. The reasons must be the researchers' own;
an AI assistant can draft the entry but shouldn't invent the reasoning.

<!--
## YYYY-MM-DD: Short title of the decision

- **Decision:** what was chosen.
- **Why:** the evidence or reasoning, e.g. a pilot comparison, a reference,
  advice from a colleague.
- **Alternatives considered:** what else was tried or rejected, and why.
- **Effect on results:** what this changes; whether earlier results need
  re-running.
- **Decided by:** who. **Links:** issue / pull request.
-->

## 2026-10-29: Report object volumes in physical units

- **Decision:** `measure` reports each object's volume in cubic units of the
  image's own voxel size (e.g. nm³), not as a voxel count.
- **Why:** volume EM voxels are often anisotropic (e.g. 8 nm in-plane, 16 nm
  between slices), so voxel counts can't be compared between datasets
  acquired at different settings.
- **Alternatives considered:** voxel counts (rejected: not comparable);
  converting everything to µm³ (deferred: units are kept as acquired, to
  avoid rounding very small objects).
- **Effect on results:** none yet; this is the template's example.
- **Decided by:** the template authors. *Replace this example entry with your
  project's first decision.*

# FAIR data: Findable, Accessible, Interoperable, Reusable

From the guide: [FAIR principles](https://ccp-volume-em.github.io/guide/fair/).

## Findable

- Capture metadata as early as possible, for datasets **and** for analyses,
  workflows, software, protocols, models and the project.
- Store acquisition metadata alongside the image data.
- Record workflow provenance: software versions, parameters, processing steps.
- Assign persistent identifiers (e.g. DOIs) to datasets and published outputs.
- Keep a consistent project structure so raw data, processed data, analyses
  and documentation are easy to find.
- Record how datasets, workflows and derived results relate to each other.
- Use OME-Zarr, which carries standard metadata and makes large datasets'
  metadata quick to explore.
- Use [RO-Crate](https://www.researchobject.org/ro-crate/) as a single entry
  point to datasets, workflows, software and documentation.

## Accessible

- Define access permissions per project or dataset.
- Keep metadata discoverable even when access to the data is restricted.
- Use standard access protocols, not custom ones.
- Document licensing, embargo periods and access requirements.
- Preserve metadata when datasets are moved or archived.

## Interoperable

- Store image data as OME-Zarr whenever possible.
- Use community vocabularies and standard metadata fields; avoid custom
  metadata formats when a standard exists.
- Describe project metadata with RO-Crate.
- Keep explicit links between datasets, workflows, software and results.
- Together, OME-Zarr and RO-Crate support submission to the
  [BioImage Archive](https://www.ebi.ac.uk/bioimage-archive/).

## Reusable

- Package datasets, workflows, software information and documentation
  together.
- Record analysis parameters and software versions, and how each output was
  generated (provenance).
- Give clear usage licences.
- Deposit completed datasets in public repositories when possible.
- An RO-Crate package should contain at least: dataset metadata, workflow
  descriptions, software and version information, provenance, licensing, and
  links between inputs, outputs and analyses.

## Resources

- [OME-Zarr / NGFF](https://ngff.openmicroscopy.org/)
- [RO-Crate specification](https://www.researchobject.org/ro-crate/specification/)
  and [Workflow RO-Crate](https://about.workflowhub.eu/Workflow-RO-Crate/)
- [BioImage Archive OME-Zarr submission guidance](https://www.ebi.ac.uk/bioimage-archive/help-zarr/)

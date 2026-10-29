# CCP-volumeEM guidance, distilled

This folder is a short, checklist-style summary of the
[CCP-volumeEM community good practice guide](https://ccp-volume-em.github.io/guide/)
([source](https://github.com/ccp-volume-em/guide)). It's written so that both
people and AI assistants can find the relevant advice quickly while working.

The guide itself is the authority. If anything here disagrees with it, the
guide wins. Each page links to the guide page it comes from.

| Read this                                                   | when you are…                                                     |
| ----------------------------------------------------------- | ----------------------------------------------------------------- |
| [software-development.md](software-development.md)          | setting up a project, organising work, writing docs and comments |
| [ai-use.md](ai-use.md)                                      | using any AI assistant, or writing an AI-use statement           |
| [testing.md](testing.md)                                    | writing or running tests, setting up CI                          |
| [ome-zarr.md](ome-zarr.md)                                  | reading or writing image data, handling metadata                 |
| [large-data-and-workflows.md](large-data-and-workflows.md)  | processing big volumes, building pipelines, HPC runs             |
| [fair-data.md](fair-data.md)                                | recording metadata and provenance, sharing data                  |
| [containers.md](containers.md)                              | writing a Dockerfile or running on HPC                           |
| [napari-plugins.md](napari-plugins.md)                      | building a napari plugin                                         |
| [publishing.md](publishing.md)                              | making the repository public, releasing, choosing a licence      |
| [green-computing.md](green-computing.md)                    | running heavy compute jobs                                       |

## Keeping this up to date

[`source.json`](source.json) records which version of the guide these pages
were written from. To check for changes:

```bash
python tools/check_guidance.py
```

To bring the pages up to date, ask your AI assistant to run the
**update-guidance** skill (`.agents/skills/update-guidance/SKILL.md`), or
follow that file's steps by hand. A scheduled GitHub Action also opens an
issue when the guide changes.

Don't put project-specific rules in these files: an update would overwrite
them. Put them in the *Project-specific notes* section of `AGENTS.md` instead.

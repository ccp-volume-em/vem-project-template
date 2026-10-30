# Development

Contributions are welcome. The full guide is
[CONTRIBUTING.md](https://github.com/ccp-volume-em/vem-project/blob/main/CONTRIBUTING.md)
in the repository.

<!-- template-example:start -->
> **Example address:** `ccp-volume-em/vem-project` is a made-up example
> project, so links and commands that use it don't work here. When you
> create your own project from the template, setup (the `start-project`
> skill) fills in your project's address automatically.
<!-- template-example:end -->

In short:

1. Work on a branch, never on `main`.
2. Make small commits with [Conventional Commit](https://www.conventionalcommits.org/) messages.
3. Add tests, and update the docs and `CHANGELOG.md`.
4. Open a pull request. It's reviewed (by a colleague where possible, or by
   yourself with the self-review checklist in REVIEWING.md) and merged.

Set up a development environment:

```bash
git clone https://github.com/ccp-volume-em/vem-project.git
cd vem-project
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest
```

Preview this documentation with `mkdocs serve`.

This project follows the
[CCP-volumeEM good practice guide](https://ccp-volume-em.github.io/guide/),
summarised in the repository's `guidance/` folder.

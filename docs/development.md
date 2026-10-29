# Development

Contributions are welcome. The full guide is
[CONTRIBUTING.md](https://github.com/ccp-volume-em/vem-project/blob/main/CONTRIBUTING.md)
in the repository. In short:

1. Work on a branch, never on `main`.
2. Make small commits with [Conventional Commit](https://www.conventionalcommits.org/) messages.
3. Add tests, and update the docs and `CHANGELOG.md`.
4. Open a pull request. A maintainer reviews and merges it.

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

# Software development

From the guide: [Software Development](https://ccp-volume-em.github.io/guide/software/).

## Collaborative development

- Host code and documentation on a platform such as GitHub, and use it for
  project management and communication too.
- Use GitHub Issues for bug reports and feature requests.
- Use feature branches and Pull Requests: one branch per change.
- Use git for version control.
- Make a release when new code is made available to users.
- Version releases as `MAJOR.MINOR.PATCH` and tag them with a `v` prefix, e.g.
  `v1.0.1` ([SemVer](https://semver.org/); [EffVer](https://jacobtomlinson.dev/effver/)
  is an alternative).
- Have a colleague review the code at important stages of development.

## Documentation

- Write both user documentation (how to use it) and developer documentation
  (how to understand and contribute to it).
- Write docs in Markdown and deploy them automatically, e.g. with
  [MkDocs](https://www.mkdocs.org/) to GitHub Pages.
- Draw diagrams with [Mermaid](https://mermaid.js.org/).

### Docstrings

- Document functions, classes and modules with docstrings, for example in
  [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html).
- Generate reference documentation from the docstrings.

### Comments

- Explain *what the function is for* and *why* the code does something.
- Don't just repeat argument names and types without adding information.
- Add inline comments wherever the what or why isn't obvious from the code.

## Containers

- Use containers (e.g. Docker) so users get a consistent, reproducible
  environment. See [containers.md](containers.md).

## Testing

- Test Python code with [pytest](https://docs.pytest.org/), run across
  environments with [tox](https://tox.wiki/), triggered automatically by a
  GitHub Action on pull request, push or release.
- Measure code coverage (e.g. pytest-cov, [Codecov](https://codecov.io/)).
  See [testing.md](testing.md).

## Maintenance

- Maintain regularly: keep dependencies up to date, fix security issues and
  bugs, update features and documentation.
- Make maintenance efficient, given limited resources: keep the code
  maintainable.
- Automate dependency and security updates with
  [Dependabot](https://github.com/dependabot) or
  [Renovate](https://docs.renovatebot.com/).

## Support

- Besides GitHub Issues, connect to one suitable community forum, e.g.
  [image.sc](https://forum.image.sc/) for image analysis software, and link to
  it from the documentation.

## AI use

See [ai-use.md](ai-use.md).

## Further resources

- [ARC Python tooling](https://github-pages.arc.ucl.ac.uk/python-tooling/)
- [The Turing Way](https://book.the-turing-way.org)
- [Software Carpentry: version control with git](https://swcarpentry.github.io/git-novice/)
- [Intermediate research software development in Python](https://carpentries-incubator.github.io/python-intermediate-development/)
- [Docker documentation](https://docs.docker.com/)
- [CCP-volumeEM: Good practices for image analysis software (video)](https://www.youtube.com/watch?v=HHJJZ79KC4Y)

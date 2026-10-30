"""Checks that project files agree with each other.

These catch common slips in a release: the version updated in one place but
not another, or the changelog losing its Unreleased section.
"""

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _pyproject_version():
    return tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]


def test_version_is_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", _pyproject_version())


def test_citation_version_matches_pyproject():
    citation = (ROOT / "CITATION.cff").read_text()
    match = re.search(r'^version:\s*"?([^"\n]+)"?', citation, re.MULTILINE)
    assert match, "CITATION.cff has no version field"
    assert match.group(1) == _pyproject_version()


def test_changelog_has_unreleased_section():
    assert "## [Unreleased]" in (ROOT / "CHANGELOG.md").read_text()


def test_guidance_source_points_at_existing_files():
    source = json.loads((ROOT / "guidance" / "source.json").read_text())
    for page, info in source["pages"].items():
        for target in info["used_in"]:
            assert (ROOT / target).is_file(), f"{page} is used in missing file {target}"


def test_guidance_pages_are_all_listed_in_agents_md():
    agents = (ROOT / "AGENTS.md").read_text()
    for page in (ROOT / "guidance").glob("*.md"):
        if page.name != "README.md":
            assert f"guidance/{page.name}" in agents, f"{page.name} is missing from AGENTS.md"


def test_skills_have_matching_names_and_descriptions():
    skills = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))
    assert skills
    for skill in skills:
        front = skill.read_text().split("---")[1]
        assert re.search(rf"^name: {skill.parent.name}$", front, re.MULTILINE), skill
        assert re.search(r"^description: .{20,}", front, re.MULTILINE), skill


def _slug(heading):
    # GitHub's anchor for a heading: lower case, punctuation dropped, spaces to hyphens.
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def _markdown_files():
    skip = {".venv", "site", ".git", "node_modules", ".tox"}
    return [p for p in ROOT.rglob("*.md") if not skip & set(p.relative_to(ROOT).parts)]


def test_relative_links_in_markdown_resolve():
    broken = []
    for page in _markdown_files():
        text = re.sub(r"```.*?```", "", page.read_text(encoding="utf-8"), flags=re.DOTALL)
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if re.match(r"[a-z]+:", target):
                continue
            path, _, anchor = target.partition("#")
            dest = (page.parent / path).resolve() if path else page
            if not dest.exists():
                broken.append(f"{page.relative_to(ROOT)}: {target}")
            elif anchor and dest.suffix == ".md":
                headings = re.findall(
                    r"^#+\s+(.*)$", dest.read_text(encoding="utf-8"), re.MULTILINE
                )
                if anchor not in {_slug(h) for h in headings}:
                    broken.append(f"{page.relative_to(ROOT)}: {target}")
    assert not broken, "broken links:\n" + "\n".join(broken)


def test_ruleset_requires_checks_that_exist():
    # A required check that no workflow runs blocks every pull request.
    ruleset = json.loads((ROOT / ".github" / "rulesets" / "main.json").read_text())
    required = [
        check["context"]
        for rule in ruleset["rules"]
        if rule["type"] == "required_status_checks"
        for check in rule["parameters"]["required_status_checks"]
    ]
    jobs = set()
    for workflow in (ROOT / ".github" / "workflows").glob("*.yml"):
        jobs.update(re.findall(r"^  ([\w-]+):$", workflow.read_text(), re.MULTILINE))
    assert required
    for context in required:
        assert context in jobs, f"the ruleset requires {context!r}, which no workflow runs"


def test_example_addresses_are_explained():
    # In the template, visitors see links to the made-up example project;
    # each page that has one says so. In a set-up project neither remains.
    placeholder = re.compile(r"ccp-volume-em/vem-project(?!-template)")
    for page in [ROOT / "README.md", ROOT / "CONTRIBUTING.md", *(ROOT / "docs").glob("*.md")]:
        text = page.read_text(encoding="utf-8")
        starts = text.count("<!-- template-example:start -->")
        assert starts == text.count("<!-- template-example:end -->"), page.name
        if placeholder.search(text):
            assert starts, f"{page.name} links to the example project without a note"

"""Checks that project files agree with each other.

These catch common slips in a release: the version updated in one place but
not another, or the changelog losing its Unreleased section.
"""

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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

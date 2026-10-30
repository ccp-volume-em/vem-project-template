"""Tests for tools/check_template.py (the parts that don't need GitHub)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_template", ROOT / "tools" / "check_template.py"
)
check_template = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_template)


@pytest.mark.parametrize(
    "url",
    [
        "git@github.com:my-lab/mito-seg.git",
        "https://github.com/my-lab/mito-seg.git",
        "https://github.com/my-lab/mito-seg",
        "ssh://git@github.com/my-lab/mito-seg.git",
    ],
)
def test_repo_slug_from_remote_urls(url):
    assert check_template.repo_slug(url) == "my-lab/mito-seg"


def test_non_github_remote_is_rejected():
    with pytest.raises(ValueError):
        check_template.repo_slug("https://gitlab.com/my-lab/mito-seg.git")


@pytest.mark.parametrize(
    "path",
    ["AGENTS.md", ".agents/skills/new-fiji-script/SKILL.md", ".github/workflows/safety.yml",
     "guidance/testing.md", "tools/check_guidance.py", "tests/repository/test_project_files.py"],
)  # fmt: skip
def test_template_maintained_files_are_shared(path):
    assert check_template.is_shared(path)


@pytest.mark.parametrize(
    "path",
    ["README.md", "pyproject.toml", "CHANGELOG.md", "src/vem_project/io.py",
     "tests/test_measure.py", "fiji/measure_object_volumes.groovy", "toolsets/x.py"],
)  # fmt: skip
def test_project_files_are_not_shared(path):
    assert not check_template.is_shared(path)


@pytest.mark.skipif(
    (ROOT / ".github" / "template.json").exists(),
    reason="a project made from the template may delete shared files it doesn't use",
)
def test_every_shared_path_exists_in_the_template():
    for shared in check_template.SHARED:
        assert (ROOT / shared).exists(), f"{shared} is listed as shared but doesn't exist"


def test_files_of_left_out_parts_are_recognised():
    left_out = check_template.left_out_files({"left_out": ["container", "unknown"]})
    assert "Dockerfile" in left_out
    assert check_template.is_left_out(".github/workflows/container.yml", left_out)
    assert check_template.is_left_out("fiji/README.md", ["fiji"])
    assert not check_template.is_left_out("fiji-tools/x.groovy", ["fiji"])
    assert check_template.left_out_files({}) == []

"""Tests for the optional parts (.github/template-parts.toml and tools/parts.py)."""

import importlib.util
import io
import json
import tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("parts", ROOT / "tools" / "parts.py")
parts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(parts)

PARTS = parts.load_parts(ROOT)


def test_parts_are_complete():
    for name, part in PARTS.items():
        for key in ("title", "question", "recommend", "shapes", "files", "edits"):
            assert part.get(key), f"part {name!r} has no {key}"
        assert set(part["shapes"]) <= {"python", "fiji"}, name


@pytest.mark.parametrize("name", PARTS)
def test_each_part_is_wholly_included_or_left_out(name):
    # The template includes every part. A project either has all of a part's
    # files or has recorded it as left out, so updates skip it.
    record = ROOT / ".github" / "template.json"
    left_out = json.loads(record.read_text())["left_out"] if record.exists() else []
    expected = "left out" if name in left_out else "included"
    assert parts.status(ROOT, PARTS[name]) == expected


@pytest.fixture
def project(tmp_path):
    """A small project made from the template, named mito-seg."""
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "template-parts.toml").write_text(
        (ROOT / ".github" / "template-parts.toml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / ".github" / "template.json").write_text(
        json.dumps({"repository": "ccp-volume-em/vem-project-template", "commit": "abc"})
    )
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "mito-seg"\n')
    (tmp_path / "src" / "mito_seg").mkdir(parents=True)
    (tmp_path / "src" / "mito_seg" / "__init__.py").write_text("")
    (tmp_path / "AGENTS.md").write_text(
        "# Rules\n\n## Project-specific notes\n\n- Uses 8 nm voxels.\n"
    )
    for f in PARTS["container"]["files"]:
        (tmp_path / f).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / f).write_text("x")
    return tmp_path


def archive(files: dict[str, str]) -> bytes:
    """A .tar.gz shaped like GitHub's archive of the template."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for path, text in files.items():
            data = text.encode()
            info = tarfile.TarInfo(f"vem-project-template-abc/{path}")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def test_remove_deletes_files_and_records_the_choice(project):
    parts.remove(project, "container")
    assert parts.status(project, PARTS["container"]) == "left out"
    assert json.loads((project / ".github" / "template.json").read_text())["left_out"] == [
        "container"
    ]
    agents = (project / "AGENTS.md").read_text()
    note = parts.note_line("container", PARTS["container"])
    assert agents.endswith("- Uses 8 nm voxels.\n" + note + "\n")


def test_add_restores_files_renamed_for_the_project(project):
    parts.remove(project, "container")
    template = archive(
        {
            "Dockerfile": (
                "<!-- template-example:start -->\nexample only\n<!-- template-example:end -->\n\n"
                'ENTRYPOINT ["vem-project"]\n# from vem_project, see '
                "https://github.com/ccp-volume-em/vem-project-template\n"
            ),
            ".dockerignore": ".git\n",
            ".github/workflows/container.yml": "name: Container\n",
            "README.md": "not part of the container\n",
        }
    )
    parts.add(project, "container", archive=template)

    assert parts.status(project, PARTS["container"]) == "included"
    assert (project / "Dockerfile").read_text() == (
        'ENTRYPOINT ["mito-seg"]\n# from mito_seg, see '
        "https://github.com/ccp-volume-em/vem-project-template\n"
    )
    assert not (project / "README.md").exists()
    assert json.loads((project / ".github" / "template.json").read_text())["left_out"] == []
    assert "Left out" not in (project / "AGENTS.md").read_text()


def test_add_keeps_existing_files(project):
    (project / "Dockerfile").write_text("the project's own")
    parts.add(project, "container", archive=archive({"Dockerfile": "the template's"}))
    assert (project / "Dockerfile").read_text() == "the project's own"


def test_parts_are_not_removed_from_the_template_itself(project):
    (project / ".github" / "template.json").unlink()
    with pytest.raises(SystemExit):
        parts.remove(project, "container")
    assert parts.status(project, PARTS["container"]) == "included"

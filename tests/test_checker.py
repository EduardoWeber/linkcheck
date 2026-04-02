from pathlib import Path

from linkcheck.checker import check_local
from linkcheck.parser import Link


def test_check_local_existing_file(tmp_path: Path):
    target = tmp_path / "docs" / "intro.md"
    target.parent.mkdir()
    target.write_text("# Intro\n")

    link = Link(text="intro", url="docs/intro.md", file=tmp_path / "readme.md", line=5)
    result = check_local(link)

    assert result.ok
    assert result.error is None


def test_check_local_missing_file(tmp_path: Path):
    link = Link(text="gone", url="missing.md", file=tmp_path / "readme.md", line=2)
    result = check_local(link)

    assert not result.ok
    assert "File not found" in result.error


def test_check_local_strips_anchor(tmp_path: Path):
    target = tmp_path / "guide.md"
    target.write_text("# Guide\n")

    link = Link(text="guide", url="guide.md#section", file=tmp_path / "index.md", line=1)
    result = check_local(link)

    assert result.ok

from click.testing import CliRunner
from pathlib import Path

from linkcheck.cli import main


def test_no_markdown_files(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path)])

    assert result.exit_code == 0
    assert "No markdown files found" in result.output


def test_no_links_in_file(tmp_path: Path):
    md = tmp_path / "empty.md"
    md.write_text("# Hello\n\nNo links here.\n")

    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path)])

    assert result.exit_code == 0
    assert "No links found" in result.output


def test_all_local_links_valid(tmp_path: Path):
    other = tmp_path / "other.md"
    other.write_text("# Other\n")

    index = tmp_path / "index.md"
    index.write_text("See [other](other.md) for details.\n")

    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--no-external"])

    assert result.exit_code == 0
    assert "1 links OK" in result.output


def test_broken_local_link_exits_nonzero(tmp_path: Path):
    md = tmp_path / "readme.md"
    md.write_text("Check [missing](nope.md) file.\n")

    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--no-external"])

    assert result.exit_code == 1
    assert "nope.md" in result.output

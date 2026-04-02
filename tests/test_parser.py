from pathlib import Path
from textwrap import dedent

from linkcheck.parser import Link, extract_links


def test_extract_links(tmp_path: Path):
    md = tmp_path / "readme.md"
    md.write_text(
        dedent("""\
        # My Project

        Check out [Google](https://google.com) and [the docs](./docs/intro.md).

        Also see [section](#overview) for more info.
        """)
    )

    links = extract_links(md)

    assert len(links) == 3
    assert links[0].url == "https://google.com"
    assert links[0].is_external
    assert links[1].url == "./docs/intro.md"
    assert not links[1].is_external
    assert links[2].is_anchor


def test_extract_no_links(tmp_path: Path):
    md = tmp_path / "empty.md"
    md.write_text("# No links here\n\nJust plain text.\n")

    assert extract_links(md) == []


def test_link_line_numbers(tmp_path: Path):
    md = tmp_path / "lines.md"
    md.write_text("line one\n\n[link](https://example.com)\n")

    links = extract_links(md)
    assert links[0].line == 3

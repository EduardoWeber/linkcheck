import re
from pathlib import Path
from dataclasses import dataclass


LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


@dataclass
class Link:
    text: str
    url: str
    file: Path
    line: int

    @property
    def is_external(self) -> bool:
        return self.url.startswith(("http://", "https://"))

    @property
    def is_anchor(self) -> bool:
        return self.url.startswith("#")


def extract_links(filepath: Path) -> list[Link]:
    """Extract all markdown links from a file."""
    links = []
    text = filepath.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in LINK_PATTERN.finditer(line):
            links.append(
                Link(
                    text=match.group(1),
                    url=match.group(2),
                    file=filepath,
                    line=lineno,
                )
            )
    return links


def find_markdown_files(directory: Path, recursive: bool = True) -> list[Path]:
    """Find all .md files in a directory."""
    pattern = "**/*.md" if recursive else "*.md"
    return sorted(directory.glob(pattern))

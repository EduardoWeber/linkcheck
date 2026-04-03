"""URL filtering utilities."""

import re
from linkcheck.parser import Link


def filter_links(
    links: list[Link],
    skip_external: bool = False,
    skip_anchors: bool = False,
    skip_patterns: list[str] | None = None,
) -> list[Link]:
    """Filter links based on criteria."""
    result = links
    if skip_external:
        result = [l for l in result if not l.is_external]
    if skip_anchors:
        result = [l for l in result if not l.is_anchor]
    if skip_patterns:
        compiled = [re.compile(p) for p in skip_patterns]
        result = [l for l in result if not any(r.search(l.url) for r in compiled)]
    return result

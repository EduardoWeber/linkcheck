"""Shared utility helpers for linkcheck."""

import re
from pathlib import Path


def normalize_url(url: str) -> str:
    """Strip fragments and trailing slashes for deduplication."""
    url = re.sub(r"#.*$", "", url)
    return url.rstrip("/")


def resolve_relative_path(base: Path, href: str) -> Path:
    """Resolve a relative href against a base file path."""
    return (base.parent / href).resolve()

"""Generate summary reports from check results."""

from linkcheck.checker import Result


def summary(results: list[Result]) -> dict:
    """Return a summary dict of check results."""
    broken = [r for r in results if not r.ok]
    return {
        "total": len(results),
        "ok": len(results) - len(broken),
        "broken": len(broken),
        "broken_urls": [r.link.url for r in broken],
    }

"""Default configuration for linkcheck."""

DEFAULTS = {
    "concurrency": 10,
    "timeout": 15.0,
    "user_agent": "linkcheck/0.4.0",
    "skip_patterns": [],
}


def get_config(**overrides) -> dict:
    """Return config with defaults merged with overrides."""
    return {**DEFAULTS, **overrides}

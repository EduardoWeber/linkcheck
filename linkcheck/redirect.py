"""Redirect handling for followed links."""

from dataclasses import dataclass


@dataclass
class RedirectConfig:
    max_redirects: int = 10
    follow: bool = True


def is_redirect(status_code: int) -> bool:
    return status_code in (301, 302, 303, 307, 308)

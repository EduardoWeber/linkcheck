"""Simple in-memory cache for URL check results."""

from dataclasses import dataclass, field
from time import monotonic


@dataclass
class CacheEntry:
    status: int | None
    ok: bool
    timestamp: float


@dataclass
class URLCache:
    ttl: float = 300.0
    _store: dict[str, CacheEntry] = field(default_factory=dict)

    def get(self, url: str) -> CacheEntry | None:
        entry = self._store.get(url)
        if entry and (monotonic() - entry.timestamp) < self.ttl:
            return entry
        return None

    def put(self, url: str, status: int | None, ok: bool) -> None:
        self._store[url] = CacheEntry(status=status, ok=ok, timestamp=monotonic())

    def clear(self) -> None:
        self._store.clear()

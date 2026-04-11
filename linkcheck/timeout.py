"""Timeout configuration for HTTP requests."""

from dataclasses import dataclass


@dataclass
class TimeoutConfig:
    connect: float = 5.0
    read: float = 10.0
    pool: float = 5.0

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.connect, self.read, self.pool)

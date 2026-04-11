"""Retry logic for failed HTTP requests."""

import asyncio
from dataclasses import dataclass, field


@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    backoff_factor: float = 2.0
    retryable_status_codes: list[int] = field(
        default_factory=lambda: [429, 500, 502, 503, 504]
    )

    async def wait(self, attempt: int) -> None:
        delay = self.base_delay * (self.backoff_factor ** attempt)
        await asyncio.sleep(delay)

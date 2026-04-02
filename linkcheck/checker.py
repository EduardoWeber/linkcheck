import asyncio
from dataclasses import dataclass
from pathlib import Path

import httpx

from linkcheck.parser import Link


@dataclass
class Result:
    link: Link
    status: int | None
    ok: bool
    error: str | None = None


async def check_url(client: httpx.AsyncClient, link: Link) -> Result:
    """Check if an external URL is reachable."""
    try:
        resp = await client.head(link.url, follow_redirects=True)
        if resp.status_code == 405:
            resp = await client.get(link.url, follow_redirects=True)
        return Result(link=link, status=resp.status_code, ok=resp.is_success)
    except httpx.RequestError as exc:
        return Result(link=link, status=None, ok=False, error=str(exc))


def check_local(link: Link) -> Result:
    """Check if a local file reference exists."""
    target = link.file.parent / link.url.split("#")[0]
    exists = target.exists()
    return Result(
        link=link,
        status=None,
        ok=exists,
        error=None if exists else f"File not found: {target}",
    )


async def check_links(
    links: list[Link],
    concurrency: int = 10,
    timeout: float = 15.0,
) -> list[Result]:
    """Check all links, external ones concurrently."""
    results: list[Result] = []
    external = [l for l in links if l.is_external]
    local = [l for l in links if not l.is_external and not l.is_anchor]

    for link in local:
        results.append(check_local(link))

    semaphore = asyncio.Semaphore(concurrency)
    headers = {"User-Agent": "linkcheck/0.4.0"}
    async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:

        async def _check(link: Link) -> Result:
            async with semaphore:
                return await check_url(client, link)

        tasks = [_check(link) for link in external]
        results.extend(await asyncio.gather(*tasks))

    return results

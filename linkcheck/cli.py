import asyncio
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from linkcheck.checker import check_links
from linkcheck.parser import extract_links, find_markdown_files

console = Console()


@click.command()
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--no-external", is_flag=True, help="Skip external URL checks")
@click.option("--skip-pattern", "-s", multiple=True, help="Regex patterns to skip")
@click.option("--concurrency", "-c", default=10, help="Max concurrent requests")
@click.option("--timeout", "-t", default=15.0, help="Request timeout in seconds")
def main(path: str, no_external: bool, concurrency: int, timeout: float) -> None:
    """Check for broken links in Markdown files."""
    target = Path(path)
    files = [target] if target.is_file() else find_markdown_files(target)

    if not files:
        console.print("[yellow]No markdown files found.[/yellow]")
        return

    console.print(f"Scanning {len(files)} file(s)...")

    all_links = []
    for f in files:
        all_links.extend(extract_links(f))

    if no_external:
        all_links = [l for l in all_links if not l.is_external]

    if not all_links:
        console.print("[green]No links found.[/green]")
        return

    results = asyncio.run(
        check_links(all_links, concurrency=concurrency, timeout=timeout)
    )
    broken = [r for r in results if not r.ok]

    if not broken:
        console.print(f"[green]All {len(results)} links OK.[/green]")
        return

    table = Table(title="Broken Links")
    table.add_column("File", style="cyan")
    table.add_column("Line", justify="right")
    table.add_column("URL", style="red")
    table.add_column("Error")

    for r in broken:
        error = r.error or f"HTTP {r.status}"
        table.add_row(str(r.link.file), str(r.link.line), r.link.url, error)

    console.print(table)
    sys.exit(1)

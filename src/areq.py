#!/usr/bin/env python3
# areq.py

"""Asynchronously get links embedded in multiple pages' HTML."""

import asyncio  # Import asyncio for handling asynchronous operations
import logging  # Import logging for debug and info logs
import re  # Import regex for parsing URLs
import sys  # Import sys for system-level operations
from typing import IO  # Import IO for type hinting file objects
import urllib.error  # Import urllib.error for handling URL-related errors
import urllib.parse  # Import urllib.parse for parsing and joining URLs

import aiofiles  # Import aiofiles for asynchronous file handling
import aiohttp  # Import aiohttp for async HTTP requests
from aiohttp import ClientSession  # Import ClientSession for handling HTTP sessions

# Configure logging settings
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")  # Create a logger instance
logging.getLogger("chardet.charsetprober").disabled = True  # Disable charset detection logs

HREF_RE = re.compile(r'href="(.*?)"')  # Regex pattern to find href links

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.
    
    kwargs are passed to `session.request()`.
    """
    resp = await session.request(method="GET", url=url, **kwargs)  # Perform GET request
    resp.raise_for_status()  # Raise exception if response status is not OK
    logger.info("Got response [%s] for URL: %s", resp.status, url)  # Log response status
    
    # Read response body asynchronously to avoid blocking the event loop.
    # This is necessary because `resp.text()` is an asynchronous coroutine.
    html = await resp.text()
    return html  # Return HTML content

async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()  # Initialize a set to store found links
    try:
        html = await fetch_html(url=url, session=session, **kwargs)  # Fetch HTML content
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )  # Log aiohttp-related exceptions
        return found
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occurred:  %s", getattr(e, "__dict__", {})
        )  # Log other exceptions
        return found
    else:
        for link in HREF_RE.findall(html):  # Extract links using regex
            try:
                abslink = urllib.parse.urljoin(url, link)  # Convert relative links to absolute
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)  # Log URL parsing errors
                pass
            else:
                found.add(abslink)  # Add valid link to the set
        logger.info("Found %d links for %s", len(found), url)  # Log number of found links
        return found  # Return set of found links

async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, **kwargs)  # Parse the URL for links
    if not res:
        return None  # Return if no links found
    async with aiofiles.open(file, "a") as f:  # Open file asynchronously in append mode
        for p in res:
            await f.write(f"{url}\t{p}\n")  # Write source URL and found URL to file
        logger.info("Wrote results for source URL: %s", url)  # Log writing completion

async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:  # Create an async HTTP session
        tasks = []  # List to store async tasks
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)  # Add write task
            )
        await asyncio.gather(*tasks)  # Run tasks concurrently

if __name__ == "__main__":
    import pathlib  # Import pathlib for file path operations
    import sys  # Import sys for version checking

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."  # Ensure Python 3.7+
    here = pathlib.Path(__file__).parent  # Get script directory path

    with open(here.joinpath("urls.txt")) as infile:  # Read URLs from file
        urls = set(map(str.strip, infile))  # Strip whitespace and store as set

    outpath = here.joinpath("foundurls.txt")  # Define output file path
    with open(outpath, "w") as outfile:  # Open output file in write mode
        outfile.write("source_url\tparsed_url\n")  # Write file header

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))  # Run async crawler

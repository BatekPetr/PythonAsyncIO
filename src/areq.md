# areq.py - Asynchronous Link Extractor

## Overview
`areq.py` is a Python script designed to asynchronously fetch and extract links (HREFs) from multiple web pages. It uses `aiohttp` for HTTP requests and `asyncio` for handling multiple operations concurrently. The extracted links are written to a file for further analysis.

## How It Works
1. **Reads URLs from `urls.txt`**
   - The script opens a file named `urls.txt` and reads URLs into a set.

2. **Fetches and Parses HTML**
   - Each URL is fetched asynchronously using `aiohttp`.
   - The HTML response is searched for `<a href="...">` links using a regular expression.

3. **Writes Results to a File**
   - Extracted links are saved in `foundurls.txt`.
   - The output format is: `source_url\tparsed_url`.

4. **Concurrency with `asyncio`**
   - Multiple pages are processed in parallel using `asyncio.gather()`, improving efficiency.

## Key Components
- `fetch_html(url, session)`: Fetches the HTML content of a URL.
- `parse(url, session)`: Extracts links from the HTML response.
- `write_one(file, url)`: Writes extracted links to a file.
- `bulk_crawl_and_write(file, urls)`: Manages concurrent crawling and writing.

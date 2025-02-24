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
- `bulk_crawl_and_write(file, urls)`: Manages concurrent crawling and 
writing.

## Understanding `resp.text()`
In `fetch_html()`, the `resp.text()` method is **awaited** because it is an **asynchronous operation**. Here's why:

- `resp.text()` is a coroutine in `aiohttp` that **reads the response body** asynchronously.
- Since the response might be large, reading it fully into memory can take time.
- Using `await` allows the event loop to **pause execution** of `fetch_html()` until the text is fully retrieved, allowing other tasks to run in the meantime.

**Correct Usage:**
```python
html = await resp.text()  # Waits for the response body to be fully received
```
- The `await` ensures that the response is **fully read before proceeding**.
- Other tasks in the event loop can continue executing while waiting for the response.

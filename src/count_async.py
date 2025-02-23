#!/usr/bin/env python3
# count_async.py
# A simple demonstration of asyncio for concurrent execution.

import asyncio

async def count():
    """Asynchronous function that prints 'One', waits for 1 second, then prints 'Two'."""
    print("One")
    await asyncio.sleep(1)  # Simulates a non-blocking delay
    print("Two")

async def main():
    """Runs three 'count' coroutines concurrently using asyncio.gather()."""
    await asyncio.gather(count(), count(), count())  # Runs all count() coroutines in parallel

if __name__ == "__main__":
    import time
    s = time.perf_counter()  # Record start time
    asyncio.run(main())  # Run the main coroutine
    elapsed = time.perf_counter() - s  # Measure elapsed time
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")  # Print execution time

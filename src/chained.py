#!/usr/bin/env python3
# chained.py
# A demonstration of asyncio chaining multiple dependent tasks.

import asyncio
import random
import time

async def part1(n: int) -> str:
    """First asynchronous task: Sleeps for a random time and returns a string result."""
    i = random.randint(0, 10)  # Generate a random sleep duration
    print(f"part1({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)  # Simulate an asynchronous delay
    result = f"result{n}-1"  # Generate result string
    print(f"Returning part1({n}) == {result}.")
    return result  # Return the result to be used in part2

async def part2(n: int, arg: str) -> str:
    """Second asynchronous task: Takes output from part1, sleeps, and returns another result."""
    i = random.randint(0, 10)  # Generate a random sleep duration
    print(f"part2{n, arg} sleeping for {i} seconds.")
    await asyncio.sleep(i)  # Simulate an asynchronous delay
    result = f"result{n}-2 derived from {arg}"  # Generate result string
    print(f"Returning part2{n, arg} == {result}.")
    return result  # Return the final result

async def chain(n: int) -> None:
    """Chains part1 and part2 together, measuring execution time."""
    start = time.perf_counter()  # Start timer
    p1 = await part1(n)  # Execute part1 and await its result
    p2 = await part2(n, p1)  # Pass part1's result to part2 and await its result
    end = time.perf_counter() - start  # Measure elapsed time
    print(f"-->Chained result{n} => {p2} (took {end:0.2f} seconds).")

async def main(*args):
    """Runs multiple chain tasks concurrently using asyncio.gather."""
    await asyncio.gather(*(chain(n) for n in args))

if __name__ == "__main__":
    import sys
    random.seed(444)  # Set random seed for reproducibility
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])  # Determine input arguments
    start = time.perf_counter()  # Start program execution timer
    asyncio.run(main(*args))  # Run the main coroutine
    end = time.perf_counter() - start  # Measure total execution time
    print(f"Program finished in {end:0.2f} seconds.")

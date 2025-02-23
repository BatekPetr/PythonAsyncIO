#!/usr/bin/env python3
# rand.py
# A demonstration of asyncio with random number generation and ANSI color formatting.

import asyncio
import random

# ANSI colors for formatted output
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

async def makerandom(idx: int, threshold: int = 6) -> int:
    """Generate a random number asynchronously, retrying if it's too low."""
    print(c[idx + 1] + f"Initiated makerandom({idx}).")  # Indicate coroutine start
    i = random.randint(0, 10)  # Generate initial random number
    
    while i <= threshold:  # Retry if below threshold
        print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
        await asyncio.sleep(idx + 1)  # Wait asynchronously before retrying
        i = random.randint(0, 10)  # Generate a new random number
    
    print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])  # Print final result
    return i  # Return the successful random number

async def main():
    """Run multiple makerandom coroutines concurrently using asyncio.gather."""
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res  # Return collected results

if __name__ == "__main__":
    random.seed(444)  # Set random seed for reproducibility
    r1, r2, r3 = asyncio.run(main())  # Run the main coroutine
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")  # Print final results

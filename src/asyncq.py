#!/usr/bin/env python3
# asyncq.py

import asyncio
import itertools as it
import os
import random
import time

# Function to generate a random item of a specified size
async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()

# Function to simulate a random sleep time between 0 and 10 seconds
async def randsleep(caller=None) -> None:
    i = random.randint(0, 10)  # Random sleep duration
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)  # Asynchronous sleep

# Producer function that generates items and adds them to the queue
async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)  # Random number of items to produce
    for _ in it.repeat(None, n):  # Loop runs n times for this producer
        await randsleep(caller=f"Producer {name}")  # Simulate work by sleeping
        i = await makeitem()  # Generate a random item
        t = time.perf_counter()  # Capture the time when item is generated
        await q.put((i, t))  # Place the item into the queue
        print(f"Producer {name} added <{i}> to queue.")  # Output to console

# Consumer function that processes items from the queue
async def consume(name: int, q: asyncio.Queue) -> None:
    while True:  # Consumer runs indefinitely until cancelled
        await randsleep(caller=f"Consumer {name}")  # Simulate work by sleeping
        i, t = await q.get()  # Retrieve item from the queue
        now = time.perf_counter()  # Capture the time when item is consumed
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")  # Output to console showing time taken
        q.task_done()  # Indicate that item has been processed

# Main function to manage producers and consumers
async def main(nprod: int, ncon: int):
    q = asyncio.Queue()  # Create a new queue to hold items
    # Create producer tasks and run them concurrently
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    # Create consumer tasks and run them concurrently
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    
    await asyncio.gather(*producers)  # Run all producers concurrently
    await q.join()  # Wait for all items to be processed (consumer task_done calls)
    
    # Cancel all consumer tasks after all produced items from the queue were processed
    for c in consumers:
        c.cancel()

# Entry point of the script when run directly
if __name__ == "__main__":
    import argparse
    random.seed(444)  # Set a fixed seed for reproducibility
    parser = argparse.ArgumentParser()  # Argument parser for command-line options
    parser.add_argument("-p", "--nprod", type=int, default=5)  # Number of producers
    parser.add_argument("-c", "--ncon", type=int, default=10)  # Number of consumers
    ns = parser.parse_args()  # Parse command-line arguments
    start = time.perf_counter()  # Record start time of the program
    asyncio.run(main(**ns.__dict__))  # Run the main function asynchronously
    elapsed = time.perf_counter() - start  # Calculate the elapsed time
    print(f"Program completed in {elapsed:0.5f} seconds.")  # Output the total time taken

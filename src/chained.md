The script [chained.py](./chained.py) demonstrates executing dependent asynchronous tasks using `asyncio` in Python. The key concept is that `part2` depends on the output of `part1`, and multiple instances of this chaining run concurrently.

## How Chaining Works

### Step 1: Executing `part1(n)`
- `part1(n)` generates a random delay (0–10 seconds).
- It sleeps asynchronously using `await asyncio.sleep(i)`, allowing other tasks to execute in the meantime.
- After sleeping, it returns a result string, e.g., `"result1-1"`.

### Step 2: Passing Output to `part2(n, arg)`
- `part2(n, arg)` receives the result of `part1(n)` as `arg`.
- It also generates a random delay before execution.
- The function produces a final output string incorporating `arg`, e.g., `"result1-2 derived from result1-1"`.

### Step 3: Timing the Execution in `chain(n)`
- `chain(n)` calls `part1(n)`, waits for its result, and then passes it to `part2(n, arg)`.
- The execution time of `chain(n)` is measured and printed.

## Concurrent Execution of Multiple Chains
- `main(*args)` runs multiple `chain(n)` tasks concurrently using `asyncio.gather()`.
- For example, calling `chain(1)`, `chain(2)`, and `chain(3)` means:
  - `part1(1)`, `part1(2)`, and `part1(3)` start together.
  - Each `part2(n, arg)` starts only after its corresponding `part1(n)` finishes.
  
## Why This Approach is Efficient
- The script **does not execute tasks sequentially** but instead **overlaps waiting times**.
- Multiple chains execute together, reducing overall runtime.
- Instead of waiting for each function call to complete before starting the next, the `async` model ensures that while one function is sleeping, others can run.

## Example Execution Flow
If `part1(1)` sleeps for 3 seconds and `part2(1, "result1-1")` sleeps for 2 seconds, the total time for `chain(1)` will be ~5 seconds. However, if `chain(2)` and `chain(3)` are running concurrently, the entire script's execution time will be closer to the longest-running chain rather than the sum of all chains.
#!/usr/bin/env python3

# The correct pattern for CPU-bound work from async code: offload to a
# ProcessPoolExecutor with loop.run_in_executor. Each call runs in its
# own OS process, sidestepping the GIL, while the event loop stays free
# to handle other coroutines. On a multi-core machine, wall time drops
# roughly to (single-task time) instead of (sum of all tasks).

import asyncio
import sys
import time
from concurrent.futures import ProcessPoolExecutor

ITERATIONS = 20_000_000


def cpu_heavy(name: str) -> str:
    total = 0
    for i in range(ITERATIONS):
        total += i * i
    return f"{name}: done (sum tail={total % 1000})"


async def main() -> None:
    loop = asyncio.get_running_loop()
    start = time.monotonic()
    with ProcessPoolExecutor() as pool:
        results = await asyncio.gather(
            *(loop.run_in_executor(pool, cpu_heavy, f"P{i}") for i in range(3))
        )
    for line in results:
        print(line)
    print(f"elapsed: {time.monotonic() - start:.2f}s")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

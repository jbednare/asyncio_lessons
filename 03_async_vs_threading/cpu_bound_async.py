#!/usr/bin/env python3

# CPU-bound work directly inside coroutines. There is no `await` in the
# hot loop, so each coroutine monopolises the event loop until it finishes.
# The three "gathered" coroutines run strictly sequentially, and wall time
# is the same as if you called them one by one. asyncio is the WRONG tool
# for CPU-bound work that runs in the same process.

import asyncio
import sys
import time

ITERATIONS = 20_000_000


async def cpu_heavy(name: str) -> None:
    print(f"{name}: start")
    total = 0
    for i in range(ITERATIONS):
        total += i * i
    print(f"{name}: done (sum tail={total % 1000})")


async def main() -> None:
    start = time.monotonic()
    await asyncio.gather(*(cpu_heavy(f"C{i}") for i in range(3)))
    print(f"elapsed: {time.monotonic() - start:.2f}s")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

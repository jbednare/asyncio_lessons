#!/usr/bin/env python3

# Same I/O-bound shape as io_bound_threading.py, but on a single thread
# with asyncio. The event loop overlaps the three asyncio.sleep calls
# cooperatively. Wall time is ~1s, with no OS threads, no locks, and
# much lower per-task overhead than threading.

import asyncio
import sys


async def worker(name: str) -> None:
    print(f"{name}: start")
    await asyncio.sleep(1)
    print(f"{name}: done")


async def main() -> None:
    await asyncio.gather(*(worker(f"A{i}") for i in range(3)))


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

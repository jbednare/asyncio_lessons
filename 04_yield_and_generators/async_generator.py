#!/usr/bin/env python3

# Putting `yield` inside an `async def` creates an ASYNC GENERATOR.
# It does both at once:
#   - `await ...`  hands control to the event loop (like any coroutine)
#   - `yield ...`  produces a value to whoever is iterating with `async for`
#
# Async generators are consumed with `async for`, not with `for` or
# `next()`. They are perfect for streams of values that arrive over
# time -- e.g., lines from a socket, rows from a paginated API.

import asyncio
import sys
import time


START = time.monotonic()


def stamp() -> str:
    return f"[t={time.monotonic() - START:.2f}s]"


async def stream_numbers(n: int):
    for i in range(n):
        await asyncio.sleep(0.5)
        print(f"{stamp()}   [producer] about to yield {i}")
        yield i


async def main() -> None:
    print(f"{stamp()} consuming async generator with `async for`:")
    async for value in stream_numbers(3):
        print(f"{stamp()} [consumer] got {value}")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

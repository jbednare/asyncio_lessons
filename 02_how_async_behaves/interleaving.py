#!/usr/bin/env python3

# Cooperative multitasking in action. Two coroutines each loop five times,
# printing a step number and yielding to the event loop with
# `await asyncio.sleep(...)`. Because they yield, the loop is free to run
# the other coroutine, so the output visibly interleaves.

import asyncio
import sys
import time


START = time.monotonic()


def stamp() -> str:
    return f"[t={time.monotonic() - START:.2f}s]"


async def ticker(name: str, delay: float, steps: int) -> None:
    for i in range(1, steps + 1):
        print(f"{stamp()} {name} step {i}/{steps}")
        await asyncio.sleep(delay)


async def main() -> None:
    await asyncio.gather(
        ticker("FAST", 0.10, 5),
        ticker("SLOW", 0.25, 5),
    )


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

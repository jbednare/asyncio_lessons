#!/usr/bin/env python3

# Two related mechanisms:
#
#   asyncio.wait_for(coro, timeout) raises asyncio.TimeoutError if the
#   coroutine does not finish in time, and cancels it.
#
#   A coroutine that is cancelled receives asyncio.CancelledError at its
#   next await. Catching it lets the coroutine clean up before exiting,
#   but it should re-raise to preserve cancellation semantics.

import asyncio
import sys
import time


START = time.monotonic()


def stamp() -> str:
    return f"[t={time.monotonic() - START:.2f}s]"


async def slow_operation(seconds: float) -> str:
    print(f"{stamp()} slow_operation: sleeping {seconds}s")
    try:
        await asyncio.sleep(seconds)
    except asyncio.CancelledError:
        print(f"{stamp()} slow_operation: got CancelledError, cleaning up")
        raise
    print(f"{stamp()} slow_operation: finished")
    return "result"


async def main() -> None:
    print(f"{stamp()} --- case 1: completes within timeout ---")
    result = await asyncio.wait_for(slow_operation(0.5), timeout=2.0)
    print(f"{stamp()} got: {result!r}\n")

    print(f"{stamp()} --- case 2: exceeds timeout ---")
    try:
        await asyncio.wait_for(slow_operation(5.0), timeout=1.0)
    except asyncio.TimeoutError:
        print(f"{stamp()} caught TimeoutError in main\n")

    print(f"{stamp()} --- case 3: explicit task cancellation ---")
    task = asyncio.create_task(slow_operation(5.0))
    await asyncio.sleep(0.3)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print(f"{stamp()} caught CancelledError in main")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

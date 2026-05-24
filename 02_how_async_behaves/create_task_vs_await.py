#!/usr/bin/env python3

# Two ways to "start" a coroutine, with very different scheduling.
#
#   await coroutine()                -> runs the coroutine to completion
#                                    before the next line of main() runs.
#   asyncio.create_task(coroutine()) -> schedules the coroutine on the loop
#                                    immediately and returns a Task. The
#                                    caller keeps running and can await
#                                    the task later.

import asyncio
import sys
import time


START = time.monotonic()


def stamp() -> str:
    return f"[t={time.monotonic() - START:.2f}s]"


async def worker(name: str, seconds: float) -> None:
    print(f"{stamp()} {name}: start, will sleep {seconds}s")
    await asyncio.sleep(seconds)
    print(f"{stamp()} {name}: done")


async def main() -> None:
    print(f"{stamp()} --- pattern 1: sequential awaits ---")
    await worker("A", 1)
    await worker("B", 1)
    print(f"{stamp()} after sequential awaits\n")

    print(f"{stamp()} --- pattern 2: create_task then await ---")
    task_c = asyncio.create_task(worker("C", 1))
    task_d = asyncio.create_task(worker("D", 1))
    print(f"{stamp()} both tasks scheduled, main() continues immediately")
    await task_c
    await task_d
    print(f"{stamp()} after awaiting both tasks")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

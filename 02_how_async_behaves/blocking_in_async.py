#!/usr/bin/env python3

# Anti-pattern: calling a blocking function (time.sleep) inside an async
# coroutine freezes the event loop. Even though we schedule three
# coroutines with asyncio.gather, they run sequentially and total ~3s.

import asyncio
import sys
import time


START = time.monotonic()


def stamp() -> str:
    return f"[t={time.monotonic() - START:.2f}s]"


async def blocking_worker(name: str) -> None:
    print(f"{stamp()} {name}: start")
    time.sleep(1)
    print(f"{stamp()} {name}: done")


async def main() -> None:
    await asyncio.gather(
        blocking_worker("A"),
        blocking_worker("B"),
        blocking_worker("C"),
    )
    print(f"{stamp()} total elapsed")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

#!/usr/bin/env python3

# Side-by-side: yield vs await.
#
#   yield  -> "here is a value, suspend until the iterator asks for the
#             next one". The consumer is a for-loop / next().
#
#   await  -> "I'm waiting for a result, suspend and let the event loop
#             run someone else until it's ready". The consumer is the
#             event loop.
#
# Both pause the function. The difference is WHO drives the resume and
# WHAT comes back: a produced value (yield) vs a returned result (await).

import asyncio
import sys
import time


START = time.monotonic()


def stamp() -> str:
    return f"[t={time.monotonic() - START:.2f}s]"


def sync_producer(n: int):
    for i in range(n):
        print(f"{stamp()}   [yield ] producing {i}")
        yield i


async def async_waiter(label: str, seconds: float) -> str:
    print(f"{stamp()}   [await ] {label}: waiting {seconds}s")
    await asyncio.sleep(seconds)
    return f"{label}-result"


async def main() -> None:
    print(f"{stamp()} --- yield: producing values to a for-loop ---")
    for value in sync_producer(3):
        print(f"{stamp()} consumed {value}")

    print(f"\n{stamp()} --- await: waiting for results from the event loop ---")
    result_a = await async_waiter("A", 0.3)
    print(f"{stamp()} got {result_a!r}")
    result_b = await async_waiter("B", 0.3)
    print(f"{stamp()} got {result_b!r}")

    print(
        f"\n{stamp()} takeaway: "
        "yield produces values; await waits for results."
    )


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

#!/usr/bin/env python3

# CPU-bound work with the threading module. Because of CPython's GIL,
# only one thread executes Python bytecode at a time, so three CPU-heavy
# threads run roughly as slowly as one big call: wall time ~= sum of
# per-thread time. Threads do NOT speed up pure-Python CPU work.

import sys
import threading
import time

ITERATIONS = 20_000_000


def cpu_heavy(name: str) -> None:
    print(f"{name}: start")
    total = 0
    for i in range(ITERATIONS):
        total += i * i
    print(f"{name}: done (sum tail={total % 1000})")


def main() -> int:
    start = time.monotonic()
    threads = [
        threading.Thread(target=cpu_heavy, args=(f"T{i}",), name=f"worker-{i}")
        for i in range(3)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"elapsed: {time.monotonic() - start:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())

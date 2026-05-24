#!/usr/bin/env python3

# I/O-bound work with the threading module. Each worker spends its time
# inside a blocking call (here: time.sleep). The OS schedules the threads
# so the blocking calls overlap. Total wall time: ~1s for three 1s
# sleeps, despite using three separate OS threads.

import sys
import threading
import time


def worker(name: str) -> None:
    print(f"{name}: start (thread={threading.current_thread().name})")
    time.sleep(1)
    print(f"{name}: done")


def main() -> int:
    threads = [
        threading.Thread(target=worker, args=(f"T{i}",), name=f"worker-{i}")
        for i in range(3)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return 0


if __name__ == "__main__":
    sys.exit(main())

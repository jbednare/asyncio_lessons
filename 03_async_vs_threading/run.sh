#!/usr/bin/sh

TIME_CMD_FORMAT="\nTotal execution time: %e seconds"

echo "============================================================"
echo "  I/O-bound: blocking sleep, three workers"
echo "============================================================"

echo "\n--- io_bound_threading.py (3 OS threads) ---\n"
time -f "${TIME_CMD_FORMAT}" ./io_bound_threading.py
echo "\n--- Done ---"

echo "\n\n--- io_bound_async.py (1 thread, asyncio.gather) ---\n"
time -f "${TIME_CMD_FORMAT}" ./io_bound_async.py
echo "\n--- Done ---"

echo "\n\n============================================================"
echo "  CPU-bound: tight Python loop, three workers"
echo "============================================================"

echo "\n--- cpu_bound_threading.py (GIL-bound, no speed-up) ---\n"
time -f "${TIME_CMD_FORMAT}" ./cpu_bound_threading.py
echo "\n--- Done ---"

echo "\n\n--- cpu_bound_async.py (event loop blocked, sequential) ---\n"
time -f "${TIME_CMD_FORMAT}" ./cpu_bound_async.py
echo "\n--- Done ---"

echo "\n\n--- cpu_bound_async_executor.py (ProcessPoolExecutor, parallel) ---\n"
time -f "${TIME_CMD_FORMAT}" ./cpu_bound_async_executor.py
echo "\n--- Done ---"

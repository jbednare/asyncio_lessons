# 03 — Async vs Threading

Same task, different concurrency models, side by side. Run `./run.sh` to
see the wall-clock times.

## I/O-bound (`time.sleep`)

| Script                       | Model                | Wall time |
| ---------------------------- | -------------------- | --------- |
| `io_bound_threading.py`      | 3 OS threads         | ~1 s      |
| `io_bound_async.py`          | 1 thread + asyncio   | ~1 s      |

Both work. Async wins on overhead (one thread, no locks, scales to
thousands of "tasks") provided every blocking call has an async
counterpart.

## CPU-bound (tight Python loop)

| Script                          | Model                         | Wall time         |
| ------------------------------- | ----------------------------- | ----------------- |
| `cpu_bound_threading.py`        | 3 OS threads (GIL serialised) | ~3 × single-task  |
| `cpu_bound_async.py`            | asyncio, no `await` in loop   | ~3 × single-task  |
| `cpu_bound_async_executor.py`   | asyncio + ProcessPoolExecutor | ~1 × single-task* |

\* on a multi-core machine.

Lessons:

- Threads do **not** speed up pure-Python CPU work because of the GIL.
- asyncio is **worse** than threads for CPU work in the same process: a
  coroutine without `await` points monopolises the event loop, so
  `gather`-ed CPU coroutines run strictly sequentially.
- Offloading CPU work to a `ProcessPoolExecutor` via `run_in_executor`
  combines the readability of async with real parallelism.

## Rule of thumb

- Many concurrent I/O operations → **asyncio**.
- Blocking I/O with no async equivalent (legacy libs, some DB drivers)
  → **threads** (or `asyncio.to_thread` / `run_in_executor`).
- Heavy CPU work → **processes** (`multiprocessing`,
  `ProcessPoolExecutor`).

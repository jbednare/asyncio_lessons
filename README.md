# asyncio examples

A progressive set of small, self-contained Python examples for learning
`asyncio`, from "what does `async def` even do" up to a real chat client
that reads from a TCP socket and the keyboard at the same time.

Each folder is independent and ships with a `run.sh` that runs the
examples (and where useful, times them with `time -f` so you can see the
wall-clock differences for yourself).

## Folders

| # | Folder                                                      | What you learn                                                                 |
| - | ----------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1 | [`01_sync_vs_async/`](01_sync_vs_async/)                    | Sync vs async; why `await` alone is not concurrency; `asyncio.gather`.         |
| 2 | [`02_how_async_behaves/`](02_how_async_behaves/)            | Event loop scheduling, blocking calls inside coroutines, `create_task` vs `await`, interleaving, cancellation and `wait_for` timeouts. |
| 3 | [`03_async_vs_threading/`](03_async_vs_threading/)          | Threads vs asyncio for I/O-bound work; the GIL and CPU-bound work; offloading via `run_in_executor` + `ProcessPoolExecutor`. |
| 4 | [`04_yield_and_generators/`](04_yield_and_generators/)      | `yield` vs `await`: sync generators, async generators (`async def` + `yield` + `async for`), and why they're different from coroutines. |
| 5 | [`05_tcp_echo_basics/`](05_tcp_echo_basics/)                | TCP server/client with `asyncio.start_server` / `asyncio.open_connection` and `StreamReader` / `StreamWriter`. |
| 6 | [`06_async_chat_client/`](06_async_chat_client/)            | Capstone: a broadcast chat with a client that reads the network and stdin concurrently on one thread. |
| 7 | [`07_multi_producer_queue/`](07_multi_producer_queue/)      | Fan-in with `asyncio.Queue`: three producers (stdin and two TCP listeners on different ports) feed one consumer engine; uses `asyncio.TaskGroup`. |

Suggested order: 1 → 2 → 3 → 4 → 5 → 6 → 7.

## Prerequisites

- Python 3.11 or newer (everything uses standard-library asyncio; no
  pip packages required; folder 7 relies on `asyncio.TaskGroup`).
- A POSIX-ish shell with GNU `time` available as `/usr/bin/time` (the
  `run.sh` scripts use `time -f "..."` for formatted output).
- For folders 6 and 7 you will want two or three terminal windows open
  at the same time so multiple clients / injectors can run alongside
  the server.

## How to run

Either run a folder's whole demo:

```sh
cd 01_sync_vs_async
./run.sh
```

Or run a single script directly:

```sh
cd 02_how_async_behaves
./interleaving.py
```

All Python scripts have shebangs and are marked executable.

## Out of scope (on purpose)

To keep these focused on the core topics above, the following are
intentionally not covered. They make great follow-up exercises:

- `async with` (async context managers); `async for` and async
  generators get an introduction in folder 4, but iterator protocols and
  `contextlib`-style helpers are not covered in depth.
- `asyncio.TaskGroup` is used in folder 7, but its error-aggregation
  semantics (exception groups, `except*`) aren't explored in detail.
- Other coordination primitives -- `asyncio.Lock`, `Semaphore`, `Event`,
  `Condition` -- get mentions but no dedicated exercises.
- Third-party async libraries such as `aiohttp`, `aiofiles`, `httpx`,
  `anyio`, `trio`.

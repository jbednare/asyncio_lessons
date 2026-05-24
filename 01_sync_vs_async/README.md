# 01 — Sync vs Async

Three runnable scripts that contrast the same task (three "sleep-and-print"
calls) written in different styles. Run `./run.sh` to see the wall-clock
difference.

## The scripts

- `non_async_sleep_print.py` — plain blocking Python. Each call to
  `time.sleep(1)` halts the whole program. Total: **~3 seconds**.
- `async_sleep_print.py` — same logic, but with `async def` and
  `await asyncio.sleep(1)`. Because each call is `await`ed *one at a time*,
  it still runs sequentially. Total: **~3 seconds**.
- `async_gather_sleep_print.py` — schedules all three coroutines together
  with `asyncio.gather(...)`. The event loop interleaves them while they
  sleep. Total: **~1 second**.

## Key concepts

- **Coroutine** — a function defined with `async def`. Calling it does not
  run it; it returns a coroutine object that must be driven by an event
  loop (via `await`, `asyncio.run`, `asyncio.gather`, `asyncio.create_task`,
  etc.).
- **Event loop** — the scheduler that runs coroutines. Started here by
  `asyncio.run(main())`. Only one coroutine runs at any instant on a
  single-threaded loop.
- **`await`** — a cooperative yield point. The current coroutine pauses
  and hands control back to the event loop, which is free to run another
  ready coroutine until the awaited operation completes.

## The big takeaway

`async`/`await` by themselves do **not** make code concurrent. They only
mark *where* the event loop is allowed to switch. You get concurrency
when you give the loop multiple coroutines to choose from — typically via
`asyncio.gather`, `asyncio.create_task`, or `asyncio.TaskGroup`.

Compare `async_sleep_print.py` (sequential awaits, ~3s) with
`async_gather_sleep_print.py` (concurrent via gather, ~1s) — same
coroutine, different scheduling, 3x speed-up.

# 02 — How Async Behaves

Four small scripts that each isolate one behavior of the asyncio event
loop. All of them print `[t=...s]` timestamps so you can see *when*
things happen, not just the order. Run `./run.sh` to execute all four
back to back with `time` measurements.

## The scripts

### `blocking_in_async.py` — anti-pattern: blocking the loop

Three coroutines are scheduled with `asyncio.gather`, but each one calls
the blocking `time.sleep(1)`. The event loop is single-threaded, so a
blocking call freezes everything; the three "concurrent" workers actually
run one after another.

- Expected wall time: **~3 s** (not 1 s).
- Rule: never call a blocking function from a coroutine without
  offloading it (e.g., `await asyncio.to_thread(blocking_fn)` or
  `loop.run_in_executor(...)`).

### `create_task_vs_await.py` — scheduling vs running

Two ways to start a coroutine, side by side:

- `await worker(...)` — runs the coroutine to completion before the next
  line of `main()` executes. Two sequential awaits → **~2 s**.
- `task = asyncio.create_task(worker(...))` — schedules the coroutine on
  the loop immediately and returns a `Task`. The caller keeps running.
  Two `create_task`s of 1 s coroutines, awaited together → **~1 s**.

Takeaway: `await coro()` is "do this now, wait for it". `create_task`
is "start this in the background, I'll wait for it later". The latter
is how you get concurrency from coroutines.

### `interleaving.py` — cooperative multitasking, visible

Two coroutines (`FAST` at 0.10 s, `SLOW` at 0.25 s) each loop and yield
to the event loop with `await asyncio.sleep(...)`. Because both yield,
the loop alternates between them, and the output visibly interleaves at
the expected timestamps. Demonstrates that switching happens **only at
`await` points**.

### `cancellation_and_timeout.py` — stopping coroutines safely

Three cases, in order:

1. `asyncio.wait_for(coro, timeout=2.0)` on a 0.5 s coroutine — finishes
   normally and returns its result.
2. `asyncio.wait_for(coro, timeout=1.0)` on a 5 s coroutine — the coroutine
   is cancelled and `main()` catches `asyncio.TimeoutError`.
3. `asyncio.create_task(...)` + manual `task.cancel()` — the coroutine
   receives `asyncio.CancelledError` at its next `await` and can do
   cleanup before re-raising.

Pattern to remember:

```python
try:
    await asyncio.sleep(seconds)
except asyncio.CancelledError:
    # ... clean up resources here ...
    raise   # re-raise so cancellation propagates
```

This is exactly the mechanism the chat client in
[`../06_async_chat_client/`](../06_async_chat_client/) uses to stop its
reader/writer tasks cleanly on disconnect.

## Key concepts in one paragraph

The event loop runs **one** coroutine at a time. `await` is a
cooperative yield: it tells the loop "I'm waiting for something, you
can run someone else until it's ready". If a coroutine never `await`s,
no one else gets to run. `create_task` schedules a coroutine so the loop
can pick it up next time it has a chance. Cancellation is delivered as
`CancelledError` at the next `await`, so well-behaved coroutines wrap
their I/O in `try`/`except` to release resources before re-raising.

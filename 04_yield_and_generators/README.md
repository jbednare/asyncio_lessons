# 04 — Yield and Generators

`yield` is the other "pause this function" keyword in Python, and it
shows up in two places that matter for asyncio: **sync generators** and
**async generators**. This folder draws the line between `yield` and
`await` so the two don't get confused.

Run `./run.sh` to execute the three scripts back to back.

## The scripts

### `sync_generator.py` — plain `yield`

A `def` with `yield` is a **generator function**. Calling it does *not*
run the body; it returns a generator object. The body advances one
chunk at a time, only when something pulls on it (via `next()` or
`for`). Trace prints show:

- Creating the generator runs no body code.
- Each `next()` runs up to (and including) the next `yield`, returns
  the value, and suspends.
- A `for` loop iterates until `StopIteration`.

Generators are **lazy**: they only do work when the consumer asks for
the next value.

### `async_generator.py` — `async def` + `yield`

Putting `yield` inside an `async def` creates an **async generator**
(PEP 525, Python 3.6+). The function can do *both*:

- `await asyncio.sleep(...)` — hands control to the event loop.
- `yield i` — produces a value to whoever is iterating with `async for`.

Async generators are the natural shape for *streams of values that
arrive over time*: lines off a socket, rows from a paginated API,
sensor readings, etc. Compare this with the streaming reader in
`[../06_async_chat_client/chat_client.py](../06_async_chat_client/chat_client.py)` —
a `while True: await reader.readline()` is essentially "the same shape
hand-written"; an async generator would let a consumer write
`async for line in incoming_lines(reader): ...` instead.

### `yield_vs_await.py` — direct side-by-side

One script with both styles back to back, with `[t=...s]` timestamps so
the difference is visible:

- A sync generator drained by a `for` loop: each `yield` produces a
  value immediately, no time passes.
- A coroutine that `await`s `asyncio.sleep(0.3)` twice: each `await`
  pauses for time to pass before the result is delivered.

## yield vs await in one table

| Construct              | Where             | Suspends to       | Consumed by             | Carries        |
| ---------------------- | ----------------- | ----------------- | ----------------------- | -------------- |
| `yield` in `def`       | sync generator    | the iterator      | `for` / `next()`        | a value out    |
| `yield` in `async def` | async generator   | the `async for`   | `async for`             | a value out    |
| `await` in `async def` | coroutine         | the event loop    | another `await` / `run` | a result back  |

## The mental model

- `yield` is about **producing values**: "here is the next item, suspend
  until the iterator asks for another".
- `await` is about **waiting for results**: "I need this to finish,
  suspend until the event loop has it for me".

Both pause the function. What differs is *who drives the resume* (an
iterator vs the event loop) and *what flows back through the pause point*
(a value the consumer takes vs a result the function receives).

# 05 — Async Chat Client (capstone)

A small broadcast chat built with `asyncio.start_server` /
`asyncio.open_connection`. The interesting part is the **client**: it
reads from the network and from the user's keyboard *at the same time*
on a single thread.

## Files

- `chat_server.py` — accepts many connections, broadcasts every received
  line to all current clients. One `handle_client` coroutine per
  connection; they all share a single `set[StreamWriter]` with no locks
  because the event loop is single-threaded.
- `chat_client.py` — connects, then runs two coroutines concurrently:
  - `read_from_server(reader)` — `await reader.readline()` loop, prints
    incoming messages.
  - `read_from_stdin(writer)` — wraps the blocking
    `sys.stdin.readline` in `loop.run_in_executor(None, ...)` so the
    event loop stays free while the user is typing. Each line is sent
    over the socket.
- `run.sh` — starts the server in the background and prints
  instructions.

## Try it

```sh
./run.sh
# then, in two more terminals:
./chat_client.py
```

Type in either client; both see the message.

## The "doing two things at once" pattern

```python
recv_task = asyncio.create_task(read_from_server(reader))
send_task = asyncio.create_task(read_from_stdin(writer))
await asyncio.wait({recv_task, send_task}, return_when=asyncio.FIRST_COMPLETED)
```

A naive `while True: line = input(); writer.write(...)` in a coroutine
would block the whole event loop on `input()` and the client would stop
receiving messages until you hit Enter. Wrapping the blocking read in
`run_in_executor` (a one-line stdlib pattern) is enough to fix it.

Alternatives, if you want to dig further:

- `aioconsole.ainput()` — same idea, nicer API, third-party dependency.
- `loop.connect_read_pipe(...)` — fully async stdin via a Protocol;
  stdlib only but more code and tricky on Windows.

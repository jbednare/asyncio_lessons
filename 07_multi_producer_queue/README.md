# 07 — Multi-Producer Queue (fan-in)

Three independent producers feed one `asyncio.Queue`; a single engine
coroutine drains it. The producers are stdin (blocking, behind a
thread) and two TCP listeners on different ports. They all push the
same `Event` shape into the same queue, and the engine doesn't have to
care where each event came from.

The two TCP producers are the same coroutine launched twice with
different labels and ports -- showing that fanning in N producers of
the same kind doesn't take more code, just more `tg.create_task(...)`
calls.

```
       CLI (stdin)           --\
                                \
       TCP listener "tcp-a"  ----+--->  asyncio.Queue[Event]  ---->  engine  -->  counts
       (port 9001)              /
                              /
       TCP listener "tcp-b"  /
       (port 9002)
```

## Files

- `[events.py](events.py)` -- the `Event` dataclass, the `EventQueue`
  type alias, and the host/port constants. Imported by everything else
  so producers, consumer, and injectors agree on the wire format.
- `[app.py](app.py)` -- the demo. Defines `cli_producer`, a single
  `tcp_producer` coroutine that takes `(queue, label, host, port)`,
  the engine, and a `main()` that launches them together in an
  `asyncio.TaskGroup`.
- `[send_tcp.py](send_tcp.py)` -- tiny helper, opens a TCP connection
  and sends three lines. Takes an optional port arg; defaults to
  `TCP_PORT_A` (9001).
- `[run.sh](run.sh)` -- starts `app.py` and prints the second-terminal
  instructions.

## How to run

In terminal A:

```sh
./run.sh
# or directly:
./app.py
```

In terminal B (any order, any number of times):

```sh
./send_tcp.py        # hits the tcp-a listener on :9001
./send_tcp.py 9002   # hits the tcp-b listener on :9002
```

In terminal A, type a line and press Enter -- that's a CLI event. Ctrl-C
to stop. The engine prints its `counts` summary on the way out.

Expected output in terminal A after running each injector once and
typing one CLI line:

```
[engine] tcp-a#1: 'hello-tcp-1'
[engine] tcp-a#2: 'hello-tcp-2'
[engine] tcp-a#3: 'hello-tcp-3'
[engine] tcp-b#1: 'hello-tcp-1'
[engine] tcp-b#2: 'hello-tcp-2'
[engine] tcp-b#3: 'hello-tcp-3'
[engine] cli#1: 'whatever you typed'
[engine] shutdown, counts={'tcp-a': 3, 'tcp-b': 3, 'cli': 1}
```

## Key teaching points

### Why `asyncio.Queue` is the natural fan-in primitive

Every producer is just `await queue.put(event)`. The engine is just
`event = await queue.get()`. There is no shared state between
producers, and the engine doesn't have to know how many producers exist
or what kind they are. New event sources plug in with no changes to the
engine: instantiate them in `main()`, hand them the queue, give them a
label.

### One coroutine, many instances

The `tcp_producer(queue, label, host, port)` coroutine is written once
and launched twice. This generalises to N: a config file listing
`(label, host, port)` triples and a loop of `tg.create_task(...)`
would let you bring up arbitrarily many TCP listeners with no extra
plumbing.

### `task_done()` and `queue.join()`

The engine calls `queue.task_done()` after handling each event. This is
not required for the queue to function, but it's how `queue.join()`
knows when all in-flight items have been processed. Useful when you
want producers to finish, then wait for the engine to fully drain
before shutting down. We don't strictly need it in this demo, but
calling `task_done()` correctly is a habit worth forming early.

### Backpressure with `Queue(maxsize=N)`

By default the queue is unbounded. Set `asyncio.Queue(maxsize=100)` and
`await queue.put(...)` will suspend the producer until the engine
catches up -- automatic backpressure with no extra code. The asyncio
documentation also lists a non-blocking `put_nowait(...)` variant that
raises `asyncio.QueueFull` if the queue is full; you'd reach for it
only inside synchronous callbacks (e.g. a `DatagramProtocol`) where
`await` isn't allowed.

### Why no locks are needed

The engine owns `counts`. It is the only coroutine that reads or writes
it. The update is a single line with no `await` between the read and
the write, so it's atomic from any other coroutine's point of view. See
`[../02_how_async_behaves/README.md](../02_how_async_behaves/README.md)`
for the general rule: *only invariants that span an `await` need a
lock*.

### See also

- `asyncio.Lock` -- mutex when a critical section must span an `await`.
- `asyncio.Semaphore` -- rate-limit the number of concurrent operations.
- `asyncio.Event` -- one-shot signal (e.g. "shutdown requested").
- `asyncio.Condition` -- wait for a predicate to become true.

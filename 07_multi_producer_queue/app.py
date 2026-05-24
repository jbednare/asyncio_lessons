#!/usr/bin/env python3

# Multi-producer, single-consumer demo. Three independent coroutines
# produce Events from different sources -- stdin and two TCP listeners
# on different ports -- and push them into the same asyncio.Queue. One
# engine coroutine drains the queue and updates its own state. Because
# the event loop runs on a single thread, and the engine never `await`s
# between reading and writing `counts`, no locks are needed.

import asyncio
import sys
import time

from events import (
    Event,
    EventQueue,
    TCP_HOST,
    TCP_PORT_A,
    TCP_PORT_B,
)


START = time.monotonic()


def stamp() -> str:
    return f"[t={time.monotonic() - START:.2f}s]"


async def cli_producer(queue: EventQueue) -> None:
    loop = asyncio.get_running_loop()
    print(f"{stamp()} [cli] reading lines from stdin (Ctrl-D to stop)")
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            print(f"{stamp()} [cli] stdin closed")
            return
        await queue.put(Event(source="cli", payload=line.rstrip("\n")))


async def tcp_producer(
    queue: EventQueue, label: str, host: str, port: int
) -> None:
    # One coroutine = one TCP listener with one label. main() spins up
    # two of these on different ports to show that fanning in N
    # producers of the same kind costs nothing extra: same code, same
    # queue, just different labels on the events.

    async def handle_conn(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        peer = writer.get_extra_info("peername")
        print(f"{stamp()} [{label}] + {peer}")
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                await queue.put(
                    Event(source=label, payload=data.decode().rstrip("\n"))
                )
        finally:
            print(f"{stamp()} [{label}] - {peer}")
            writer.close()
            try:
                await writer.wait_closed()
            except (ConnectionError, OSError):
                pass

    server = await asyncio.start_server(handle_conn, host, port)
    print(f"{stamp()} [{label}] listening on {host}:{port}")
    async with server:
        await server.serve_forever()


async def engine(queue: EventQueue) -> None:
    counts: dict[str, int] = {}
    print(f"{stamp()} [engine] starting, waiting for events")
    try:
        while True:
            event = await queue.get()
            counts[event.source] = counts.get(event.source, 0) + 1
            print(
                f"{stamp()} [engine] {event.source}#{counts[event.source]}: "
                f"{event.payload!r}"
            )
            queue.task_done()
    except asyncio.CancelledError:
        print(f"{stamp()} [engine] shutdown, counts={counts}")
        raise


async def main() -> None:
    queue: EventQueue = asyncio.Queue()
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(engine(queue), name="engine")
            tg.create_task(cli_producer(queue), name="cli")
            tg.create_task(
                tcp_producer(queue, "tcp-a", TCP_HOST, TCP_PORT_A),
                name="tcp-a",
            )
            tg.create_task(
                tcp_producer(queue, "tcp-b", TCP_HOST, TCP_PORT_B),
                name="tcp-b",
            )
    except* KeyboardInterrupt:
        print(f"{stamp()} [main] interrupted")


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n[main] bye")

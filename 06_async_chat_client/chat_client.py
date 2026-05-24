#!/usr/bin/env python3

# Interactive chat client that does two things at once on a single
# event-loop thread:
#
#   1. read_from_server: awaits incoming lines from the TCP socket and
#      prints them.
#   2. read_from_stdin:  awaits the user's next line of input and sends
#      it over the socket.
#
# Naively calling input() inside a coroutine would block the whole event
# loop and freeze incoming messages. Instead we hand sys.stdin.readline
# off to the default thread executor via loop.run_in_executor(...) and
# await the resulting Future. That keeps the loop responsive.
#
# Alternatives worth knowing about:
#   - aioconsole.ainput(): same idea, prettier API, third-party dep.
#   - loop.connect_read_pipe(...): full async stdin via a Protocol;
#     stdlib-only but more code, and tricky on Windows.

import asyncio
import sys


HOST = "127.0.0.1"
PORT = 8888


async def read_from_server(reader: asyncio.StreamReader) -> None:
    while True:
        data = await reader.readline()
        if not data:
            print("\n[server closed the connection]")
            return
        sys.stdout.write(data.decode())
        sys.stdout.flush()


async def read_from_stdin(writer: asyncio.StreamWriter) -> None:
    loop = asyncio.get_running_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            print("[stdin closed]")
            return
        writer.write(line.encode())
        await writer.drain()


async def main() -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f"client: connected to {HOST}:{PORT}. Type messages and press Enter.")
    print("client: press Ctrl-C to quit.\n")

    recv_task = asyncio.create_task(read_from_server(reader))
    send_task = asyncio.create_task(read_from_stdin(writer))

    done, pending = await asyncio.wait(
        {recv_task, send_task}, return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()
    for task in pending:
        try:
            await task
        except asyncio.CancelledError:
            pass

    writer.close()
    try:
        await writer.wait_closed()
    except (ConnectionError, OSError):
        pass


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nclient: interrupted, bye")

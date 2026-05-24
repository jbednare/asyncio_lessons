#!/usr/bin/env python3

# Smallest possible asyncio TCP client. Opens a connection, sends one
# line, awaits the echoed reply, then closes. Demonstrates the
# StreamReader / StreamWriter pair returned by asyncio.open_connection.

import asyncio
import sys


HOST = "127.0.0.1"
PORT = 8888
MESSAGE = "hello from echo_client\n"


async def main() -> None:
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f"client: connected to {HOST}:{PORT}")

    print(f"client: -> {MESSAGE!r}")
    writer.write(MESSAGE.encode())
    await writer.drain()

    reply = await reader.readline()
    print(f"client: <- {reply.decode()!r}")

    writer.close()
    await writer.wait_closed()
    print("client: closed")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

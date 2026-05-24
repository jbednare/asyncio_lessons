#!/usr/bin/env python3

# Minimal asyncio TCP echo server using the high-level streams API.
# asyncio.start_server() spawns a fresh `handle_client` coroutine for
# every accepted connection, so many clients can be served concurrently
# on a single thread.

import asyncio
import sys


HOST = "127.0.0.1"
PORT = 8888


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    peer = writer.get_extra_info("peername")
    print(f"server: connection from {peer}")
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode().rstrip("\n")
            print(f"server: <- {peer} {message!r}")
            writer.write(data)
            await writer.drain()
    finally:
        print(f"server: closing {peer}")
        writer.close()
        await writer.wait_closed()


async def main() -> None:
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addrs = ", ".join(str(s.getsockname()) for s in server.sockets)
    print(f"server: listening on {addrs}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nserver: interrupted, shutting down")

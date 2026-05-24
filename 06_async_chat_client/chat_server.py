#!/usr/bin/env python3

# A broadcast chat server. Every line received from a client is forwarded
# to all currently connected clients (including the sender, so they see
# their own message arrive over the socket). asyncio.start_server spawns
# one handle_client coroutine per connection; they all share the CLIENTS
# set. Because everything runs on a single event-loop thread, no locks
# are needed to mutate that set.

import asyncio
import sys


HOST = "127.0.0.1"
PORT = 8888

CLIENTS: set[asyncio.StreamWriter] = set()


async def broadcast(message: bytes, sender_label: str) -> None:
    print(f"server: broadcasting from {sender_label}: {message!r}")
    stale: list[asyncio.StreamWriter] = []
    for writer in CLIENTS:
        if writer.is_closing():
            stale.append(writer)
            continue
        try:
            writer.write(message)
            await writer.drain()
        except (ConnectionError, OSError):
            stale.append(writer)
    for writer in stale:
        CLIENTS.discard(writer)


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    peer = writer.get_extra_info("peername")
    label = f"{peer[0]}:{peer[1]}"
    CLIENTS.add(writer)
    print(f"server: + {label} connected ({len(CLIENTS)} total)")
    await broadcast(f"*** {label} joined\n".encode(), sender_label="server")
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            await broadcast(f"[{label}] ".encode() + data, sender_label=label)
    finally:
        CLIENTS.discard(writer)
        print(f"server: - {label} disconnected ({len(CLIENTS)} total)")
        await broadcast(f"*** {label} left\n".encode(), sender_label="server")
        writer.close()
        try:
            await writer.wait_closed()
        except (ConnectionError, OSError):
            pass


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

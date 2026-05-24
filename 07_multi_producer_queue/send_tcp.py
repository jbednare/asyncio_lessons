#!/usr/bin/env python3

# Injector helper: connect to one of the TCP producers in app.py and
# send three lines, then close. Run while app.py is up.
#
# Usage:
#   ./send_tcp.py            # connects to TCP_PORT_A (the default)
#   ./send_tcp.py 9002       # connects to the given port (e.g. tcp-b)

import asyncio
import sys

from events import TCP_HOST, TCP_PORT_A


LINES = ["hello-tcp-1", "hello-tcp-2", "hello-tcp-3"]


async def main(port: int) -> None:
    reader, writer = await asyncio.open_connection(TCP_HOST, port)
    print(f"send_tcp: connected to {TCP_HOST}:{port}")
    for line in LINES:
        writer.write(f"{line}\n".encode())
        await writer.drain()
        print(f"send_tcp: -> {line!r}")
    writer.close()
    await writer.wait_closed()
    print("send_tcp: done")
    _ = reader


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else TCP_PORT_A
    sys.exit(asyncio.run(main(port)))

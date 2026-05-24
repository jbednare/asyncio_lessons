# Shared types for app.py and the injector helpers. Keeping the Event
# shape in one place means a producer can never disagree with the engine
# about what an event looks like.

import asyncio
from dataclasses import dataclass, field
from time import monotonic


@dataclass(frozen=True)
class Event:
    source: str
    payload: str
    received_at: float = field(default_factory=monotonic)


EventQueue = asyncio.Queue[Event]


TCP_HOST = "127.0.0.1"
TCP_PORT_A = 9001
TCP_PORT_B = 9002

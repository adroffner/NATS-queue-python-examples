""" NATS: Publish/Subscribe with JSON Payloads
"""

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import (
    # ErrConnectionClosed,
    # ErrTimeout,
    ErrNoServers
)

from producer_consumer.message_json import publish_json, message_handler


async def run(loop):
    nc = NATS()

    await nc.connect("127.0.0.1:4222", loop=loop)

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("foo.queue", cb=message_handler)

    # Stop receiving after 2 messages.
    await nc.auto_unsubscribe(sid, 2)
    await publish_json(nc, "foo.queue", {
        "hello": "world",
        "sincere": True
    })
    await publish_json(nc, "foo.queue", {
        "hello": "fool!",
        "sincere": False,
        "age": 1002
    })

    # Drain topic(s) and Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    d = {
        "hello": "world",
        "sincere": True
    }
    print('Cold in the D! ', d)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()

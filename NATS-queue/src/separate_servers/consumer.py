""" Consumer Server
"""

import traceback

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import (
    ErrConnectionClosed,
    ErrTimeout,
    ErrNoServers
)

NATS_USER = 'your'
NATS_PASS = 'mom'
# NATS_USER = 'admin'
# NATS_PASS = 'hello'

PUB_SUBJECT = 'com.example.updates'


async def consumer_action():
    nc = NATS()

    async def error_cb(e):
        if not isinstance(e, asyncio.InvalidStateError):
            print(traceback.format_exc())
        else:
            print("Probably waiting for messages and not done...")

    await nc.connect(servers=["nats://127.0.0.1:4222"],
                     user=NATS_USER, password=NATS_PASS,
                     error_cb=error_cb,
                     connect_timeout=3)

    future = asyncio.Future()

    async def cb(msg):
        nonlocal future
        future.set_result(msg)

    await nc.subscribe(PUB_SUBJECT, cb=cb)

    # Wait for message to arrive and return it.
    try:
        timeout = None  # seconds
        msg = await asyncio.wait_for(future, timeout)
    except (ErrConnectionClosed, ErrTimeout, ErrNoServers):
        return None

    return msg


async def main():
    for msg_number in range(1, 10):
        message = await consumer_action()
        print('NATS Message [{}]'.format(message.data))


if __name__ == '__main__':
    asyncio.run(main())

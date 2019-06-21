""" Publisher Server
"""

from datetime import datetime

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import (
    # ErrConnectionClosed,
    # ErrTimeout,
    ErrNoServers
)

# NATS_USER = 'the'
# NATS_PASS = 'fuzz'
NATS_USER = 'admin'
NATS_PASS = 'hello'

PUB_SUBJECT = 'com.example.updates'


async def publish_message(msg_bytes):
    nc = NATS()

    async def error_cb(e):
        print(e)
        raise e

    await nc.connect(servers=["nats://127.0.0.1:4222"],
                     user=NATS_USER, password=NATS_PASS,
                     error_cb=error_cb,
                     connect_timeout=3)

    await nc.publish(PUB_SUBJECT, msg_bytes)
    await nc.flush()

    await nc.drain()

if __name__ == '__main__':
    asyncio.run(publish_message(datetime.utcnow().isoformat().encode()))
    print('NATS Published Message ...')

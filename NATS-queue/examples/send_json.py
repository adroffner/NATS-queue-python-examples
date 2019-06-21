""" NATS: Publish/Subscribe with JSON Payloads
"""

import json

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import (
    # ErrConnectionClosed,
    # ErrTimeout,
    ErrNoServers
)


def pack_json(json_dict):
    return json.dumps(json_dict).encode()


def unpack_json(json_bytes):
    return json.loads(json_bytes.decode('utf8'))


async def run(loop):
    nc = NATS()

    await nc.connect("127.0.0.1:4222", loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = unpack_json(msg.data)
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("foo.json", cb=message_handler)

    # Stop receiving after 2 messages.
    await nc.auto_unsubscribe(sid, 2)
    await nc.publish("foo.json", pack_json({
        "hello": "world",
        "sincere": True
    }))
    await nc.publish("foo.json", pack_json({
        "hello": "fool!",
        "sincere": False,
        "age": 1002
    }))

    # Drain topic(s) and Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    d = pack_json({
        "hello": "world",
        "sincere": True
    })
    print('Cold in the D! ', d)
    print('Unpack It: ', unpack_json(b'{"hello": "world", "sincere": true}'))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()

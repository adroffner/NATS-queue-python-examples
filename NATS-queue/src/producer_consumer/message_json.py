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


async def message_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = unpack_json(msg.data)
    print("Received a message on '{subject} {reply}': {data}".format(
        subject=subject, reply=reply, data=data))


async def publish_json(nats_client, topic_name, payload_json):
    await nats_client.publish(topic_name, pack_json(payload_json))

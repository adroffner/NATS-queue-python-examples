""" NATS: Publish/Subscribe with JSON Payloads
"""

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import (
    # ErrConnectionClosed,
    # ErrTimeout,
    ErrNoServers
)

from producer_consumer.message_json import unpack_json, publish_json


class SerializableThing(object):
    """ Serializable Thing.

    This class can serialize its object to JSON and send them over a NATS subject.
    """

    def message_handler(self, msg):
        """ NATS message_handler callback

        Use this message_handler to subscribe and pass objects.

        serializable_thing = SerializableThing()
        sid = await nc.subscribe("subject", cb=serializable_thing.message_handler)

        :param msg: is a NATS message object
        """

        self._subject = msg.subject
        self._reply = msg.reply
        json_dict = unpack_json(msg.data)

        for k, v in json_dict.items():
            setattr(self, k, v)

    def __str__(self):
        return 'SerializableThing: {}'.format({k: v for k, v in self.__dict__.items()})


async def run(loop):
    nc = NATS()

    await nc.connect("127.0.0.1:4222", loop=loop)

    # Simple publisher and async subscriber via coroutine.
    serializable_thing = SerializableThing()
    print('New SerializableThing: {}'.format(serializable_thing))
    sid = await nc.subscribe("foo.queue", cb=serializable_thing.message_handler)

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
    print('Messaged SerializableThing: {}'.format(serializable_thing))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()

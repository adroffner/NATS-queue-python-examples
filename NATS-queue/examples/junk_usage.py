import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import (
    # ErrConnectionClosed,
    ErrTimeout,
    ErrNoServers
)


async def run(loop):
    nc = NATS()

    await nc.connect("127.0.0.1:4222", loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("foo", cb=message_handler)

    # Stop receiving after 2 messages.
    # await nc.auto_unsubscribe(sid, 3)
    await nc.publish("foo", b'Hello')
    await nc.publish("foo", b'World')
    await nc.publish("foo", b'!!!!!')

    """
    requests = []
    for i in range(0, 1):
        request = nc.request("foo", b'?', timeout=3)
        requests.append(request)

    # Wait for all the responses
    responses = []
    responses = await asyncio.gather(*requests)
    print("Responses:\n", responses)
    """

    # Gracefully close the connection.
    await nc.drain()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()

NATS Publish/Subscribe: Separate Servers
========================================

This **python3.7** example shows how _separate services_
communicate over a **publish-subscribe** _subject_.

* **consumer.py** waits for the _publisher_ to send a message.
* **publisher.py** sends (_publishes_) a message over the _subject_ queue.

Running the Example
-------------------

This example requires _two independent_ **python3.7** programs
to run concurrently. The **consumer.py** one **must start first**!

### Consumer Server

``` bash
python3.7 consumer.py
```

### Publisher Server

``` bash
python3.7 publisher.py

for k in {1..10}; do
    echo "Publish message number $k ..."
    python3.7 ./publisher.py
    echo
done
```

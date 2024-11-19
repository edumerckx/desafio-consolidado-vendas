import os

import pika


class RabbitMQConsumer:
    def __init__(self, str_conn, queue, callback, prefetch_count=1):
        self._str_conn = str_conn
        self._queue = queue
        self._callback = callback
        self._prefetch_count = prefetch_count
        self._channel = self._create_channel()

    def _create_channel(self):
        conn = pika.BlockingConnection(pika.URLParameters(self._str_conn))
        channel = conn.channel()

        channel.queue_declare(
            queue=self._queue,
            durable=True,
        )

        channel.basic_qos(prefetch_count=self._prefetch_count)

        channel.basic_consume(
            queue=self._queue,
            on_message_callback=self._callback,
        )

        return channel

    def start(self):
        try:
            print('# Consumer started...')
            self._channel.start_consuming()
        except KeyboardInterrupt:
            print('# Consumer stopped...')
            os._exit(0)
        # except Exception as e:
        #     print(f'# Error: {e.with_traceback()}')

    def __del__(self):
        self._channel.close()

import pika


class RabbitMQPublisher:
    def __init__(self, str_conn, exchange, queue):
        # print(f'===== \n\t{str_conn}\n\t{exchange}\n\t{queue}')
        self._str_conn = str_conn
        self._exchange = exchange
        self._queue = queue
        self._channel = self._create_channel()

    def _create_channel(self):
        conn = pika.BlockingConnection(pika.URLParameters(self._str_conn))
        channel = conn.channel()

        channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='fanout',
        )
        channel.queue_declare(
            queue=self._queue,
            durable=True,
        )
        channel.queue_bind(
            exchange=self._exchange,
            queue=self._queue,
        )

        return channel

    def publish(self, body):
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key='',
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
        )

    def __del__(self):
        self._channel.close()

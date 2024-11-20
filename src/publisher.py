import json

import requests

from rabbitmq_publisher import RabbitMQPublisher
from settings import Settings

settings = Settings()


def get_seller_data():
    try:
        resp = requests.get(Settings().SELLERS_ENDPOINT)
        return resp.json()
    except requests.exceptions.JSONDecodeError:
        return []


def process_sellers(sellers):
    print(f'# {len(sellers)} sellers will be processed')
    if len(sellers) > 0:
        publisher = RabbitMQPublisher(
            str_conn=settings.AMQP_URL,
            exchange=settings.EXCHANGE_SELLERS,
            queue=settings.QUEUE_SELLERS,
        )

        for seller in sellers:
            publisher.publish(json.dumps(seller))


if __name__ == '__main__':
    sellers_data = get_seller_data()
    process_sellers(sellers_data)

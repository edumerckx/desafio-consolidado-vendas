import json

import requests

from rabbitmq_publisher import RabbitMQPublisher
from settings import Settings

settings = Settings()


def get_seller_data():
    resp = requests.get(Settings().SELLERS_ENDPOINT)
    return resp.json()


def process_sellers(sellers):
    publisher = RabbitMQPublisher(
        str_conn=settings.AMQP_URL,
        exchange=settings.EXCHANGE_SELLERS,
        queue=settings.QUEUE_SELLERS,
    )
    for seller in sellers:
        print(f'# seller {seller['nome']}')
        publisher.publish(json.dumps(seller))


if __name__ == '__main__':
    # print(type(Settings().CLIENTS_ENDPOINT))
    sellers_data = get_seller_data()
    process_sellers(sellers_data)

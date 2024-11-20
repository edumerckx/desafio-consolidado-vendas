import asyncio
import json
import os
import time

import pandas as pd
from httpx import AsyncClient

from rabbitmq_consumer import RabbitMQConsumer
from settings import Settings

settings = Settings()

os.makedirs('consolidado', exist_ok=True)


async def process_seller(seller):
    async with AsyncClient() as client:
        resp = await client.get(
            f'{settings.SALES_ENDPOINT}?vendedor_id={seller["id"]}'
        )
        df_sales = pd.DataFrame(resp.json())

        list_client_ids = set(df_sales['cliente_id'])
        list_product_ids = set(df_sales['produto_id'])

        clients = []
        for client_id in list_client_ids:
            resp = await client.get(
                f'{settings.CLIENTS_ENDPOINT}?id={client_id}'
            )
            clients.append(resp.json()[0])
        df_clients = pd.DataFrame(clients)
        df_clients.rename(lambda x: f'cliente_{x}', axis=1, inplace=True)

        products = []
        for product_id in list_product_ids:
            resp = await client.get(
                f'{settings.PRODUCTS_ENDPOINT}?id={product_id}'
            )
            products.append(resp.json()[0])
        df_products = pd.DataFrame(products)
        df_products.rename(lambda x: f'produto_{x}', axis=1, inplace=True)

        df = pd.merge(df_sales, df_clients, how='inner', on='cliente_id')
        df['vendedor_nome'] = seller['nome']
        df['vendedor_telefone'] = seller['telefone']

        df = df.merge(df_products, how='inner', on='produto_id')
        columns = [
            'vendedor_id',
            'vendedor_nome',
            'vendedor_telefone',
            'cliente_id',
            'cliente_nome',
            'cliente_telefone',
            'cliente_email',
            'produto_id',
            'produto_nome',
            'produto_preco',
            'produto_sku',
        ]

        df = df[columns]
        df.to_csv(
            f'consolidado/{seller["id"]}-{seller["nome"]}.csv',
            index=False,
            header=True,
        )


def on_message(channel, method, properties, body):
    seller = json.loads(body)

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_seller(seller))

        print(f'# Seller {seller['nome']} processed')
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        print(f'# Error - Seller {seller['nome']} not processed - requeue - waiting for {settings.DELAY_IN_SECONDS} second(s)')  # noqa: E501
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
        time.sleep(settings.DELAY_IN_SECONDS)


if __name__ == '__main__':
    consumer = RabbitMQConsumer(
        str_conn=settings.AMQP_URL,
        queue=settings.QUEUE_SELLERS,
        callback=on_message,
    )
    consumer.start()

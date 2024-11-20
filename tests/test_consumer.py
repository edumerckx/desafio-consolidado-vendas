import pandas as pd
import pytest
from httpx import AsyncClient, Response

from src.consumer import (
    get_clients_data,
    get_products_data,
    get_sales_data,
    process_seller,
)
from src.settings import Settings

settings = Settings()


@pytest.mark.asyncio
async def test_get_clients_data(respx_mock):
    async with AsyncClient() as client:
        mock_data = [
            {
                'nome': 'Nome Teste',
                'telefone': '12345678',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
        respx_mock.get(f'{settings.CLIENTS_ENDPOINT}?id=1').mock(
            return_value=Response(200, json=mock_data)
        )

        df_clients = await get_clients_data(list_client_ids=[1], client=client)

    expected_columns = [
        'cliente_nome',
        'cliente_telefone',
        'cliente_email',
        'cliente_id',
    ]
    assert df_clients.shape == (1, 4)
    assert df_clients.columns.to_list() == expected_columns


@pytest.mark.asyncio
async def test_get_products_data(respx_mock):
    async with AsyncClient() as client:
        mock_data = [
            {
                'nome': 'Produto',
                'tipo': 'test',
                'preco': 10.0,
                'sku': '123',
                'vendedor_id': 1,
                'id': 1,
            }
        ]
        respx_mock.get(f'{settings.PRODUCTS_ENDPOINT}?id=1').mock(
            return_value=Response(200, json=mock_data)
        )

        df_clients = await get_products_data(
            list_product_ids=[1], client=client
        )

    expected_columns = [
        'produto_nome',
        'produto_tipo',
        'produto_preco',
        'produto_sku',
        'produto_vendedor_id',
        'produto_id',
    ]
    assert df_clients.shape == (1, 6)
    assert df_clients.columns.to_list() == expected_columns


@pytest.mark.asyncio
async def test_get_sales_data(respx_mock):
    async with AsyncClient() as client:
        mock_data = [
            {
                'vendedor_id': 1,
                'cliente_id': 1,
                'produto_id': 1,
                'id': 1,
            }
        ]
        respx_mock.get(f'{settings.SALES_ENDPOINT}?vendedor_id=1').mock(
            return_value=Response(200, json=mock_data)
        )

        df_clients = await get_sales_data(seller_id=1, client=client)

    expected_columns = [
        'vendedor_id',
        'cliente_id',
        'produto_id',
        'id',
    ]
    assert df_clients.shape == (1, 4)
    assert df_clients.columns.to_list() == expected_columns


@pytest.mark.asyncio
async def test_process_seller(mocker):
    sales_data = [
        {
            'vendedor_id': 1,
            'cliente_id': 1,
            'produto_id': 1,
            'id': 1,
        }
    ]
    sales_data = pd.DataFrame(sales_data)
    get_sales_data = mocker.patch(
        'src.consumer.get_sales_data',
        return_value=sales_data,
    )

    clients_data = [
        {
            'cliente_nome': 'Nome Teste',
            'cliente_telefone': '12345678',
            'cliente_email': 'test@test.com',
            'cliente_id': 1,
        }
    ]
    clients_data = pd.DataFrame(clients_data)
    get_clients_data = mocker.patch(
        'src.consumer.get_clients_data',
        return_value=clients_data,
    )

    products_data = [
        {
            'produto_nome': 'Produto',
            'produto_tipo': 'test',
            'produto_preco': 10.0,
            'produto_sku': '123',
            'produto_vendedor_id': 1,
            'produto_id': 1,
        }
    ]
    products_data = pd.DataFrame(products_data)
    get_products_data = mocker.patch(
        'src.consumer.get_products_data',
        return_value=products_data,
    )

    mocker.patch('pandas.DataFrame.to_csv')

    seller = {
        'id': 1,
        'nome': 'test',
        'telefone': '12345678',
    }
    await process_seller(seller)

    assert get_sales_data.called
    assert get_clients_data.called
    assert get_products_data.called
    pd.DataFrame.to_csv.assert_called_once_with(
        f'consolidado/{seller["id"]}-{seller["nome"]}.csv',
        index=False,
        header=True,
    )


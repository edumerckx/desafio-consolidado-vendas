import builtins
import json

from src.publisher import get_seller_data, process_sellers
from src.rabbitmq_publisher import RabbitMQPublisher


def test_get_seller_data(mocker):
    mock_data = [{'nome': 'Nome Teste'}]

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data

    mocker.patch('httpx.get', return_value=mock_response)
    seller_data = get_seller_data()

    assert seller_data == mock_data


def test_get_seller_data_empty(mocker):
    mock_response = mocker.MagicMock()
    mock_response.json = Exception('test')

    mocker.patch('httpx.get', return_value=mock_response)
    seller_data = get_seller_data()

    assert seller_data == []


def test_process_sellers_empty(mocker):
    spy = mocker.spy(builtins, 'print')

    process_sellers([])

    assert spy.call_count == 1
    assert spy.call_args() == ('# 0 sellers will be processed',)


def test_process_sellers_publish(mocker):
    class FakeRabbitMQPublisher:
        def publish(self, body):  # noqa: PLR6301
            assert json.loads(body) == {'nome': 'test'}

    fake_class = FakeRabbitMQPublisher()

    mocker.patch.object(RabbitMQPublisher, '__new__', return_value=fake_class)

    process_sellers([{'nome': 'test'}])

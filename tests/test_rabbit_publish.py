import json
import unittest
from unittest.mock import patch, MagicMock
from app import rabbit

class TestRabbitPublish(unittest.TestCase):
    def setUp(self):
        rabbit.RabbitMQ._connection = None
        rabbit.RabbitMQ._channel = None

    @patch("app.rabbit.pika.BlockingConnection")
    @patch("app.rabbit.pika.URLParameters")
    @patch("app.rabbit.pika.BasicProperties")
    def test_publish_calls_correctly(self, MockProps, MockURLParams, MockConn):
        mock_channel = MagicMock()
        mock_conn_instance = MagicMock()
        mock_conn_instance.channel.return_value = mock_channel
        MockConn.return_value = mock_conn_instance

        queue_name = "fila.notificacao.entrada.JULIANA"
        message = json.dumps({"traceId": "t-1", "mensagemId": "m-1"})

        rabbit.RabbitMQ.publish(queue_name, message)

        MockConn.assert_called_once()
        mock_conn_instance.channel.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue=queue_name, durable=True)
        MockProps.assert_called_once_with(delivery_mode=2)
        mock_channel.basic_publish.assert_called_once_with(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=MockProps.return_value
        )
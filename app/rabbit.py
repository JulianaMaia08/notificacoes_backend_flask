import pika
import os

RABBIT_URL = os.getenv("RABBIT_URL")

class RabbitMQ:

    _connection = None
    _channel = None

    @classmethod
    def get_channel(cls):
        if cls._connection is None or cls._connection.is_closed:
            cls._connection = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
            cls._channel = cls._connection.channel()
        return cls._channel
    
    @classmethod
    def publish(cls, queue_name, message):
        channel = cls.get_channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
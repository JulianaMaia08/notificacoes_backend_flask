import pika
import json
from rabbit import RabbitMQ

QUEUE_DLQ = "fila.notificacao.dlq.JULIANA"

def processar_dlq(ch, method, properties, body):
    message = json.loads(body)
    traceId = message["traceId"]
    print(f"Mensagem {traceId} foi para DLQ e não será processada novamente")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consumir_dlq():
    channel = RabbitMQ.get_channel()
    channel.queue_declare(queue=QUEUE_DLQ, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_DLQ, on_message_callback=processar_dlq)
    print(f"Consumindo fila: {QUEUE_DLQ}")
    channel.start_consuming()

if __name__ == "__main__":
    consumir_dlq()

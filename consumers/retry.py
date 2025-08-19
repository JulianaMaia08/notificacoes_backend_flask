import pika
import json
import time
import random
from storage import notifications
from rabbit import RabbitMQ

QUEUE_RETRY = "fila.notificacao.retry.JULIANA"
QUEUE_VALIDACAO = "fila.notificacao.validacao.JULIANA"
QUEUE_DLQ = "fila.notificacao.dlq.JULIANA"

def processar_retry(ch, method, properties, body):
    message = json.loads(body)
    traceId = message["traceId"]

    time.sleep(3)

    if random.random() < 0.2:
        print(f"Falha no reprocessamento da mensagem {traceId}")
        notifications[traceId]["status"] = "FALHA_FINAL_REPROCESSAMENTO"
        RabbitMQ.publish(QUEUE_DLQ, body)
    else:
        print(f"Mensagem {traceId} reprocessada com sucesso")
        notifications[traceId]["status"] = "REPROCESSADO_COM_SUCESSO"
        RabbitMQ.publish(QUEUE_VALIDACAO, body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumir_retry():
    channel = RabbitMQ.get_channel()
    channel.queue_declare(queue=QUEUE_RETRY, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_RETRY, on_message_callback=processar_retry)
    print(f"Consumindo fila: {QUEUE_RETRY}")
    channel.start_consuming()


if __name__ == "__main__":
    consumir_retry()
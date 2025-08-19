import pika
import json
import time
import random
from storage import notifications
from rabbit import RabbitMQ

QUEUE_ENTRADA = "fila.notificacao.entrada.JULIANA"
QUEUE_RETRY = "fila.notificacao.retry.JULIANA"
QUEUE_VALIDACAO = "fila.notificacao.validacao.JULIANA"

def processar_mensagem(ch, method, properties, body):
    message = json.loads(body)
    traceId = message["traceId"]

    if random.random() < 0.12:
        print(f"Falha no processamento inicial da mensagem {traceId}")
        notifications[traceId]["status"] = "FALHA_PROCESSAMENTO_INICIAL"
        RabbitMQ.publish(QUEUE_RETRY, body)
    else:
        time.sleep(random.uniform(1, 1.5))
        notifications[traceId]["status"] = "PROCESSADO_INTERMEDIARIO"
        RabbitMQ.publish(QUEUE_VALIDACAO, body)
        print(f"Mensagem {traceId} processada com sucesso")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumir_fila():
    channel = RabbitMQ.get_channel()
    channel.queue_declare(queue=QUEUE_ENTRADA, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_ENTRADA, on_message_callback=processar_mensagem)
    print(f"Consumindo fila: {QUEUE_ENTRADA}")
    channel.start_consuming()


if __name__ == "__main__":
    consumir_fila()
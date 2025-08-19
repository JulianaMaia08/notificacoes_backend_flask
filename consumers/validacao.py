import pika
import json
import time
import random
from storage import notifications
from rabbit import RabbitMQ

QUEUE_VALIDACAO = "fila.notificacao.validacao.JULIANA"
QUEUE_DLQ = "fila.notificacao.dlq.JULIANA"

def processar_validacao(ch, method, properties, body):
    message = json.loads(body)
    traceId = message["traceId"]

    # Simula envio real com tempo aleatório
    time.sleep(random.uniform(0.5, 1))
    
    # Chance de falha no envio (5%)
    if random.random() < 0.05:
        print(f"Falha no envio final da mensagem {traceId}")
        notifications[traceId]["status"] = "FALHA_ENVIO_FINAL"
        RabbitMQ.publish(QUEUE_DLQ, body)
    else:
        print(f"Mensagem {traceId} enviada com sucesso")
        notifications[traceId]["status"] = "ENVIADO_SUCESSO"

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumir_validacao():
    channel = RabbitMQ.get_channel()
    channel.queue_declare(queue=QUEUE_VALIDACAO, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_VALIDACAO, on_message_callback=processar_validacao)
    print(f"Consumindo fila: {QUEUE_VALIDACAO}")
    channel.start_consuming()


if __name__ == "__main__":
    consumir_validacao()
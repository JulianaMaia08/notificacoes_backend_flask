# Notificações Backend - Flask + RabbitMQ

Projeto de backend em **Python/Flask** para envio e processamento assíncrono de notificações usando **RabbitMQ**.  

O backend permite:  

- Receber requisições HTTP para criar notificações (`POST /api/notificar`)  
- Rastrear o status de cada notificação (`GET /api/notificacao/status/<traceId>`)  
- Publicar mensagens em filas RabbitMQ para processamento assíncrono  
- Simular pipelines com retry e Dead Letter Queue (DLQ) em memória  
- Testar o fluxo com **unittest** e mocks, sem depender de RabbitMQ real  

---

## Tecnologias usadas

- Python 3.10+  
- Flask  
- RabbitMQ (via `pika`)  
- UUID para identificação de mensagens  
- Unittest + mocks para testes  

---



from flask import Flask, request, jsonify
from uuid import uuid4
from .storage import notifications
from .rabbit import RabbitMQ
import json

app = Flask(__name__)

QUEUE_ENTRADA = "fila.notificacao.entrada.JULIANA"

@app.route("/api/notificar", methods=["POST"])
def notificar():
    data = request.get_json()

    if not data or "conteudoMensagem" not in data or "tipoNotificacao" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    traceId = str(uuid4())
    mensagemId = data.get("mensagemId") or str(uuid4())


    notifications[traceId] = {
        "mensagemId": mensagemId,
        "conteudoMensagem": data["conteudoMensagem"],
        "tipoNotificacao": data["tipoNotificacao"],
        "status": "RECEBIDO"
    }


    message = {
        "traceId": traceId,
        "mensagemId": mensagemId,
        "conteudoMensagem": data["conteudoMensagem"],
        "tipoNotificacao": data["tipoNotificacao"]
    }


    RabbitMQ.publish(QUEUE_ENTRADA, json.dumps(message))

    return jsonify({"mensagemId": mensagemId, "traceId": traceId}), 202

@app.route("/api/notificacao/status/<traceId>", methods=["GET"])
def notificacao_status(traceId):
    notification = notifications.get(traceId)

    if not notification:
        return jsonify({'error': 'traceId nao encontrado'}), 404
    
    notif_copy = notification.copy()
    if isinstance(notif_copy.get("tipoNotificacao"), set):
        notif_copy["tipoNotificacao"] = list(notif_copy["tipoNotificacao"])

    return jsonify({
        "traceId": traceId,
        "mensagemId": notif_copy["mensagemId"],
        "conteudoMensagem": notif_copy["conteudoMensagem"],
        "tipoNotificacao": notif_copy["tipoNotificacao"],
        "status": notif_copy["status"]
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
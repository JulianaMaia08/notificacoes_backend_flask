import unittest
from unittest.mock import patch
from app.main import app, notifications
import json

class TestNotificationFlow(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        notifications.clear()

    @patch("app.main.RabbitMQ.publish")
    def test_post_and_get_notification(self, mock_publish):
        payload = {"conteudoMensagem": "Teste de notificação", "tipoNotificacao": ["EMAIL"]}
        post_resp = self.client.post("/api/notificar", json=payload)
        self.assertEqual(post_resp.status_code, 202)
        post_data = post_resp.get_json()
        traceId = post_data["traceId"]

        mock_publish.assert_called_once()

        get_resp = self.client.get(f"/api/notificacao/status/{traceId}")
        self.assertEqual(get_resp.status_code, 200)
        get_data = get_resp.get_json()

        self.assertEqual(get_data["traceId"], traceId)
        self.assertEqual(get_data["conteudoMensagem"], "Teste de notificação")
        self.assertEqual(get_data["tipoNotificacao"], ["EMAIL"])
        self.assertEqual(get_data["status"], "RECEBIDO")

    def test_get_nonexistent_traceId(self):
        resp = self.client.get("/api/notificacao/status/nao-existe")
        self.assertEqual(resp.status_code, 404)
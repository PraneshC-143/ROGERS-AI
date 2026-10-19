import io
import os
import unittest
from unittest.mock import patch

from app import app


class RogersAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_loads_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('ROGERS-01'.encode(), response.data)

    def test_health_route(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['status'], 'online')
        self.assertEqual(payload['assistant'], 'ROGERS-01')
        self.assertIn('ai_configured', payload)

    def test_chat_demo_mode_without_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post('/api/chat', json={'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['mode'], 'demo')
        self.assertIn('OPENAI_API_KEY', payload['reply'])

    def test_chat_rejects_empty_message(self):
        response = self.client.post('/api/chat', json={'message': '   '})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertIn('error', payload)

    def test_analyze_accepts_supported_text_file(self):
        data = {
            'file': (io.BytesIO(b'line one\nline two'), 'notes.txt')
        }
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post('/api/analyze', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['filename'], 'notes.txt')
        self.assertEqual(payload['mode'], 'demo')
        self.assertIn('File received successfully', payload['analysis'])

    def test_analyze_rejects_invalid_input(self):
        response = self.client.post('/api/analyze', data={}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

        bad_file_data = {
            'file': (io.BytesIO(b'binary'), 'archive.zip')
        }
        response = self.client.post('/api/analyze', data=bad_file_data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 415)


if __name__ == '__main__':
    unittest.main()

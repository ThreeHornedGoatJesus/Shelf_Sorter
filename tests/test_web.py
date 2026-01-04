import unittest

try:
    from web_app import app
    flask_available = True
except Exception:
    app = None
    flask_available = False

class TestWebUI(unittest.TestCase):
    def test_index(self):
        if not flask_available:
            self.skipTest('Flask not available')
        client = app.test_client()
        r = client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_pack_api(self):
        if not flask_available:
            self.skipTest('Flask not available')
        client = app.test_client()
        payload = { 'box': {'w':200,'h':100}, 'items':[{'w':30,'h':20,'count':5}] }
        r = client.post('/pack', json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn('placements', data)
        self.assertGreater(len(data['placements']), 0)

if __name__ == '__main__':
    unittest.main()

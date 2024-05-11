import unittest
from flask_testing import TestCase
from app import create_app

class BaseTestCase(TestCase):

    def create_app(self):
        app, _ = create_app()
        app.config.update({
            "TESTING": True,
            "MONGO_URI": "mongodb://localhost:27017/health_db_test",
            "WTF_CSRF_ENABLED": False,
            "DEBUG": False
        })
        return app

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Health Monitoring API is running!', response.data)

if __name__ == '__main__':
    unittest.main()

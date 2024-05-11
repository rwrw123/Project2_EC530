from test_basic import BaseTestCase
import unittest

class DeviceRoutesTestCase(BaseTestCase):

    def setUp(self):
        self.device_data = {
            "type": "ECG",
            "model": "HeartMonitor3000"
        }

    def test_register_device(self):
        response = self.client.post('/devices/register', json=self.device_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

if __name__ == '__main__':
    unittest.main()

from test_basic import BaseTestCase
import unittest

class PatientRoutesTestCase(BaseTestCase):

    def setUp(self):
        self.patient_id = 12345
        self.app.mongo.db.patients.insert_one({
            "patient_id": self.patient_id,
            "name": "Zoe Doe"
        })

    def tearDown(self):
        self.app.mongo.db.measurements.delete_many({})
        self.app.mongo.db.patients.delete_many({})
        self.app.mongo.db.appointments.delete_many({})

    def test_submit_measurement(self):
        response = self.client.post(f'/patients/{self.patient_id}/measurements/add', json={
            "type": "Blood Pressure",
            "value": 120
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_book_appointment(self):
        response = self.client.post(f'/patients/{self.patient_id}/appointments/book', json={
            "mpId": 1,
            "time": "2024-06-01T14:30:00Z"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

if __name__ == '__main__':
    unittest.main()

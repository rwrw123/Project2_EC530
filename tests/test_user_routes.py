from test_basic import BaseTestCase
from bson.objectid import ObjectId
import unittest

class UserRoutesTestCase(BaseTestCase):

    def setUp(self):
        self.user_data = {
            "name": "Zoe Doe",
            "email": "zdoe@example.com",
            "roles": ["admin"]
        }
        self.test_user_id = str(self.app.mongo.db.users.insert_one(self.user_data).inserted_id)

    def tearDown(self):
        """ Clean up test user """
        self.app.mongo.db.users.delete_many({})

    def test_user_addition(self):
        response = self.client.post('/users/add', json={
            "name": "Zoe Doe",
            "email": "zdoe@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_assign_role(self):
        response = self.client.post(f'/users/{self.test_user_id}/assignRole', json={
            "roles": ["editor", "viewer"]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

if __name__ == '__main__':
    unittest.main()



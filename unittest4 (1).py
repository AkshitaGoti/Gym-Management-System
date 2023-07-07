import unittest

from flask import Flask

from app import app


class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_add_member_route(self):
        response = self.client.post('/add_member', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)

    def test_view_member_route(self):
        response = self.client.get('/view_member')
        self.assertEqual(response.status_code, 200)


    def test_delete_view_member_route(self):
        response = self.client.post('/delete_view_member', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)


    def test_my_trainer_schedule_route(self):
        response = self.client.get('/trainer__shedule')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

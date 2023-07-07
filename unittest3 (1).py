import unittest

from flask import Flask

from app import app


class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        

    def test_discover_route(self):
        response = self.client.get('/discover')
        self.assertEqual(response.status_code, 200)
        

    def test_profile_route(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        

    def test_edit_profile_route(self):
        response = self.client.get('/edit_profile')
        self.assertEqual(response.status_code, 200)
        

    def test_view_equipment_route(self):
        response = self.client.get('/view_equipment')
        self.assertEqual(response.status_code, 200)
        


if __name__ == '__main__':
    unittest.main()

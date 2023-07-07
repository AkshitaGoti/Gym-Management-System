import unittest

from flask import Flask, render_template, request

from app import app


class GymManagementSystemRouteTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_add_trainer_route(self):
        response = self.app.get('/add_trainer')
        self.assertEqual(response.status_code, 200)

    def test_add_member_route(self):
        response = self.app.get('/add_member')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

import unittest

from flask import Flask, render_template, request

from app import app


class AdminPanelRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        pass
    
    def test_admin_route(self):
        response = self.app.get('/admin')
        self.assertEqual(response.status_code, 200)

    
    def test_add_trainer_route(self):
        response = self.app.get('/add_trainer')
        self.assertEqual(response.status_code, 200)

    
    def test_delete_trainer_route(self):
        response = self.app.get('/delete_trainer')
        self.assertEqual(response.status_code, 200)

    
    def test_new_equip_route(self):
        response = self.app.get('/new_equip')
        self.assertEqual(response.status_code, 200)

    
    def test_delete_equip_route(self):
        response = self.app.get('/delete_equip')
        self.assertEqual(response.status_code, 200)

    
    def test_view_staff_route(self):
        response = self.app.get('/view_staff')
        self.assertEqual(response.status_code, 200)

    
    def test_add_trainer_shedule_route(self):
        response = self.app.get('/add_trainer_shedule')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

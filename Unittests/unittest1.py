import sqlite3
import unittest


class GymManagementSystemUnitTest(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect('Database.db')  # Connect to the database
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()  # Close the database connection

    def test_user_authentication(self):
        # Test user authentication
        username = 'hemu'
        password = '123'
        
        self.cursor.execute("SELECT * FROM login WHERE username=? AND password=?", (username, password))
        result = self.cursor.fetchone()
        
        self.assertIsNotNone(result)  # Check if the login is successful

    def test_member_profile_management(self):
        # Test member profile management
        username = 'hemu'
        email = 'hmanral265@gmail.com'
        age = '25'
        
        self.cursor.execute("INSERT INTO Profile (username, email, age) VALUES (?, ?, ?)", (username, email, age))
        self.conn.commit()
        
        self.cursor.execute("SELECT * FROM Profile WHERE username=?", (username,))
        result = self.cursor.fetchone()
        
        self.assertEqual(result[2], email)  # Check if the email is correctly stored in the profile

    def test_equipment_inventory_management(self):
        # Test equipment inventory management
        equip_name = 'Dumbbells'
        
        self.cursor.execute("SELECT * FROM Equipments WHERE Equip_name=?", (equip_name,))
        result = self.cursor.fetchone()
        
        self.assertIsNotNone(result)  # Check if the equipment exists in the inventory

    def test_feedback_collection(self):
        # Test feedback collection
        name = 'John Doe'
        message = 'Great gym facilities!'
        
        self.cursor.execute("INSERT INTO feedback (name, message) VALUES (?, ?)", (name, message))
        self.conn.commit()
        
        self.cursor.execute("SELECT * FROM feedback WHERE name=?", (name,))
        result = self.cursor.fetchone()
        
        self.assertEqual(result[1], message)  # Check if the message is correctly stored in the feedback

if __name__ == '__main__':
    unittest.main()

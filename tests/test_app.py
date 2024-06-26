import unittest
import json
from app import app, db
from views import User, Item

class InventoryManagerTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client and initialize the database
        self.app = app.test_client()
        self.app.testing = True
        
        # Push an application context
        self.app_context = app.app_context()
        self.app_context.push()
        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

        # Add a test user
        user = User(username='testuser', password='testpassword', role='user')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        # Remove the database session and drop all tables
        db.session.remove()
        db.drop_all()
        
        # Pop the application context
        self.app_context.pop()

    def test_register(self):
        response = self.app.post('/api/register', data=json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User registered successfully')

    def test_login(self):
        response = self.app.post('/api/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Login successful')

    def test_login_invalid_credentials(self):
        response = self.app.post('/api/login', data=json.dumps({
            'username': 'testuser',
            'password': 'wrongpassword'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid credentials')

    def test_add_item(self):
        response = self.app.post('/api/items', data=json.dumps({
            'name': 'Test Item',
            'quantity': 10
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Item added successfully')

    def test_get_items(self):
        # First, add an item
        self.app.post('/api/items', data=json.dumps({
            'name': 'Test Item',
            'quantity': 10
        }), content_type='application/json')

        # Then, retrieve the items
        response = self.app.get('/api/items')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Item')
        self.assertEqual(data[0]['quantity'], 10)

    def test_update_item(self):
        # First, add an item
        response = self.app.post('/api/items', data=json.dumps({
            'name': 'Test Item',
            'quantity': 10
        }), content_type='application/json')
        item_id = json.loads(response.data)['id']

        # Then, update the item
        response = self.app.put(f'/api/items/{item_id}', data=json.dumps({
            'name': 'Updated Test Item',
            'quantity': 5
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Item updated successfully')

    def test_delete_item(self):
        # First, add an item
        response = self.app.post('/api/items', data=json.dumps({
            'name': 'Test Item',
            'quantity': 10
        }), content_type='application/json')
        item_id = json.loads(response.data)['id']

        # Then, delete the item
        response = self.app.delete(f'/api/items/{item_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Item deleted successfully')

if __name__ == '__main__':
    unittest.main()


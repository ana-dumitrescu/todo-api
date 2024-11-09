import pytest
import os
import tempfile
from app import create_app, db
from app.models.user import User
from app.models.todo import Todo
import json
from datetime import datetime

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
    
    # Create tables
    with app.app_context():
        db.create_all()
        
    yield app
    
    # Clean up
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    # Register a user
    user_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    client.post('/api/register', json=user_data)
    
    # Login and get token
    response = client.post('/api/login', json=user_data)
    return response.get_json()['access_token']

class TestAuth:
    def test_register(self, client):
        response = client.post('/api/register', json={
            'email': 'new@example.com',
            'password': 'password123'
        })
        assert response.status_code == 201
        assert 'message' in response.get_json()

    def test_register_duplicate_email(self, client):
        # Register first user
        client.post('/api/register', json={
            'email': 'duplicate@example.com',
            'password': 'password123'
        })
        
        # Try to register same email
        response = client.post('/api/register', json={
            'email': 'duplicate@example.com',
            'password': 'password123'
        })
        assert response.status_code == 409

    def test_login_success(self, client):
        # Register user
        client.post('/api/register', json={
            'email': 'login@example.com',
            'password': 'password123'
        })
        
        # Login
        response = client.post('/api/login', json={
            'email': 'login@example.com',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert 'access_token' in response.get_json()

    def test_login_invalid_credentials(self, client):
        response = client.post('/api/login', json={
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401

    def test_register_invalid_email(self, client):
        response = client.post('/api/register', json={
            'email': 'invalid_email',
            'password': 'password123'
        })
        assert response.status_code == 400

    def test_register_short_password(self, client):
        response = client.post('/api/register', json={
            'email': 'test@example.com',
            'password': '12345'
        })
        assert response.status_code == 400

    def test_login_missing_fields(self, client):
        response = client.post('/api/login', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400

        response = client.post('/api/login', json={
            'password': 'password123'
        })
        assert response.status_code == 400

class TestTodos:
    def test_create_todo(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/todos', json={
            'title': 'Test Todo',
            'description': 'Test Description',
            'priority': 'high'
        }, headers=headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Test Todo'
        assert data['priority'] == 'high'

    def test_get_todos(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a todo first
        client.post('/api/todos', json={
            'title': 'Test Todo'
        }, headers=headers)
        
        # Get todos
        response = client.get('/api/todos', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_update_todo(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a todo
        response = client.post('/api/todos', json={
            'title': 'Original Title'
        }, headers=headers)
        todo_id = response.get_json()['id']
        
        # Update todo
        response = client.put(f'/api/todos/{todo_id}', json={
            'title': 'Updated Title',
            'completed': True
        }, headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Title'
        assert data['completed'] == True

    def test_delete_todo(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a todo
        response = client.post('/api/todos', json={
            'title': 'To Be Deleted'
        }, headers=headers)
        todo_id = response.get_json()['id']
        
        # Delete todo
        response = client.delete(f'/api/todos/{todo_id}', headers=headers)
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f'/api/todos/{todo_id}', headers=headers)
        assert response.status_code == 404

    def test_create_todo_without_title(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/todos', json={
            'description': 'Test Description'
        }, headers=headers)
        assert response.status_code == 400

    def test_create_todo_with_invalid_priority(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/todos', json={
            'title': 'Test Todo',
            'priority': 'invalid'
        }, headers=headers)
        assert response.status_code == 400

    def test_update_todo_not_found(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.put('/api/todos/9999', json={
            'title': 'Updated Title'
        }, headers=headers)
        assert response.status_code == 404

    def test_delete_todo_not_found(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.delete('/api/todos/9999', headers=headers)
        assert response.status_code == 404

    def test_get_todo_not_found(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/todos/9999', headers=headers)
        assert response.status_code == 404

    def test_unauthorized_access(self, client):
        # Try to access without token
        response = client.get('/api/todos')
        assert response.status_code == 401

        # Try with invalid token
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.get('/api/todos', headers=headers)
        assert response.status_code == 422
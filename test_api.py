import requests
import json
from datetime import datetime, timedelta
import time

BASE_URL = 'http://localhost:5000/api'

def print_test_result(operation, response):
    print(f"\n{'='*20} {operation} {'='*20}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print('='*50)

def test_api():
    # 1. Test Registration
    print("\nTesting User Registration...")
    register_data = {
        "email": f"test_{int(time.time())}@example.com",  # Unique email
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print_test_result("Registration", response)
    
    # 2. Test Login
    print("\nTesting Login...")
    response = requests.post(f"{BASE_URL}/login", json=register_data)
    print_test_result("Login", response)
    
    assert response.status_code == 200, "Login failed!"
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 3. Test Todo Creation
    print("\nTesting Todo Creation...")
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item",
        "priority": "high",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=headers)
    print_test_result("Create Todo", response)
    
    assert response.status_code == 201, "Todo creation failed!"
    todo_id = response.json()['id']
    
    # 4. Test Get All Todos
    print("\nTesting Get All Todos...")
    response = requests.get(f"{BASE_URL}/todos", headers=headers)
    print_test_result("Get All Todos", response)
    
    # 5. Test Get Single Todo
    print("\nTesting Get Single Todo...")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers=headers)
    print_test_result("Get Single Todo", response)
    
    # 6. Test Update Todo
    print("\nTesting Update Todo...")
    update_data = {
        "title": "Updated Todo",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data, headers=headers)
    print_test_result("Update Todo", response)
    
    # 7. Test Delete Todo
    print("\nTesting Delete Todo...")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}", headers=headers)
    print_test_result("Delete Todo", response)
    
    # 8. Verify Todo is Deleted
    print("\nVerifying Todo is Deleted...")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers=headers)
    print_test_result("Get Deleted Todo", response)
    
    print("\nAPI Testing Complete!")

if __name__ == "__main__":
    test_api()
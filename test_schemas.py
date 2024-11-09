from app.schemas.todo import TodoSchema
from app.schemas.user import UserSchema, LoginSchema
from datetime import datetime

def test_schemas():
    print("Testing schemas...")
    
    # Test TodoSchema
    todo_data = {
        'title': 'Test Todo',
        'description': 'Testing schemas',
        'priority': 'high',
        'completed': False
    }
    
    todo_schema = TodoSchema()
    result = todo_schema.load(todo_data)
    print("\nTodo Schema Test:")
    print(f"Input: {todo_data}")
    print(f"Validated: {result}")
    
    print("\nTests completed successfully!")

if __name__ == '__main__':
    test_schemas()
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.todo import Todo
from app import db
from datetime import datetime

todos_bp = Blueprint('todos', __name__)

VALID_PRIORITIES = ['low', 'medium', 'high']

@todos_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([todo.to_dict() for todo in todos])

@todos_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    # Validate priority if provided
    if 'priority' in data and data['priority'] not in VALID_PRIORITIES:
        return jsonify({'error': f'Priority must be one of: {", ".join(VALID_PRIORITIES)}'}), 400
        
    new_todo = Todo(
        title=data.get('title'),
        description=data.get('description', ''),
        completed=data.get('completed', False),
        priority=data.get('priority', 'medium'),
        user_id=user_id
    )
    
    if data.get('due_date'):
        try:
            new_todo.due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify(new_todo.to_dict()), 201

@todos_bp.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    return jsonify(todo.to_dict())

@todos_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    data = request.get_json()

    # Validate priority if provided
    if 'priority' in data and data['priority'] not in VALID_PRIORITIES:
        return jsonify({'error': f'Priority must be one of: {", ".join(VALID_PRIORITIES)}'}), 400
    
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed']
    if 'priority' in data:
        todo.priority = data['priority']
    if 'due_date' in data:
        try:
            todo.due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    db.session.commit()
    return jsonify(todo.to_dict())

@todos_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return '', 204
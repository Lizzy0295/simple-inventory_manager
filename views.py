from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token

db = SQLAlchemy()  # Create a SQLAlchemy instance without app context

auth_bp = Blueprint('auth', __name__)
item_bp = Blueprint('item', __name__)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)

# Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = generate_password_hash(data.get('password'))
    role = data.get('role', 'user')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity={'username': user.username, 'role': user.role})
    return jsonify({'message': 'Login successful', 'access_token': access_token})

# Add item route
@item_bp.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    
    if not name or quantity is None:
        return jsonify({'message': 'Name and quantity are required'}), 400
    
    item = Item(name=name, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    
    return jsonify({'message': 'Item added successfully', 'id': item.id}), 201

# Get all items route
@item_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    result = [{'id': item.id, 'name': item.name, 'quantity': item.quantity} for item in items]
    return jsonify(result)

# Update item route
@item_bp.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = Item.query.get(id)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    item.name = data.get('name', item.name)
    item.quantity = data.get('quantity', item.quantity)
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})

# Delete item route
@item_bp.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})


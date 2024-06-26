from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Import blueprints
from views import auth_bp, item_bp  # Importing after initializing app and db

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(item_bp, url_prefix='/item')

# Create all tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


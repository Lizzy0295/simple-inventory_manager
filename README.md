# simple-inventory_manager
Project Portfolio


Simple Inventory Manager
Overview
The Simple Inventory Manager is a web-based application for managing an inventory of items. It allows users to register, log in, add items, view the inventory list, update item details, and delete items. The application is built with Flask, SQLAlchemy, and includes a simple HTML/CSS frontend.

Features
User Registration and Login
Add, View, Update, and Delete Inventory Items
Simple and Intuitive User Interface

Installation
Clone the repository:
git clone https://github.com/yourusername/simple-inventory-manager.git
cd simple-inventory-manager
Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the dependencies:

pip install -r requirements.txt

Run the application:
python app.py
The application will be running at http://127.0.0.1:5000/.

Directory Structure
inventory_manager/
|-- app.py
|-- views.py
|-- templates/
|   |-- index.html
|-- static/
|   |-- styles.css
|-- tests/
|   |-- test_app.py
|-- requirements.txt
|-- README.md



Usage
Open your web browser and go to http://127.0.0.1:5000/.
Register a new user.
Log in with the registered user credentials.
Add new items to the inventory.
View the list of items, update item details, or delete items.

API Endpoints
/api/register (POST): Register a new user.
/api/login (POST): Log in a user.
/api/items (GET): Get a list of all items.
/api/items (POST): Add a new item.
/api/items/<id> (PUT): Update an item.
/api/items/<id> (DELETE): Delete an item.
Running Tests

Navigate to the project directory:
cd simple-inventory_manager

Run the tests:
python -m unittest discover -s tests


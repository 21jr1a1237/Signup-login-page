from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['mydb']
users_collection = db['data']

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle index logic
@app.route('/index', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Find the user in the database
    user = users_collection.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        return 'Login successful!'
    else:
        return 'Invalid username or password', 401

# Route to add a new user to MongoDB (this could be part of a signup process)
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    # Check if user already exists
    if users_collection.find_one({'username': username}):
        return 'User already exists', 400

    # Insert the new user into the database
    users_collection.insert_one({'username': username, 'password': hashed_password})
    return 'User registered successfully!'

if __name__ == '__main__':
    app.run(debug=True)
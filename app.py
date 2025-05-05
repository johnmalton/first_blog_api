import datetime
from flask import Flask, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# In-memory storage for users and posts (replace with a database in production)
users = []
posts = []


@app.route("/", methods=["GET"])
def index():
    return jsonify(message="Hello Ai Class")

# Function to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Route to register a new user (signup)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = {'username': data['username'], 'password': hashed_password}
    users.append(new_user)
    return jsonify({'message': 'User registered successfully!'}), 201

# Route to login and get a JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    for user in users:
        if user['username'] == data['username'] and check_password_hash(user['password'], data['password']):
            token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Create a new post
@app.route('/post', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()
    new_post = {
        'id': len(posts) + 1,  # Simple ID generation
        'title': data['title'],
        'content': data['content'],
        'author': current_user
    }
    posts.append(new_post)
    return jsonify({'message': 'Post created successfully!', 'post': new_post}), 201

# Get all posts
@app.route('/posts', methods=['GET'])
@token_required
def get_posts(current_user):
    return jsonify({'posts': posts}), 200

# Get a single post by ID
@app.route('/post/<int:id>', methods=['GET'])
@token_required
def get_post(current_user, id):
    post = next((post for post in posts if post['id'] == id), None)
    if post:
        return jsonify({'post': post}), 200
    return jsonify({'message': 'Post not found'}), 404

# Update a post
@app.route('/post/<int:id>', methods=['PUT'])
@token_required
def update_post(current_user, id):
    data = request.get_json()
    post = next((post for post in posts if post['id'] == id), None)
    if post:
        post['title'] = data.get('title', post['title'])
        post['content'] = data.get('content', post['content'])
        return jsonify({'message': 'Post updated successfully!', 'post': post}), 200
    return jsonify({'message': 'Post not found'}), 404

# Delete a post
@app.route('/post/<int:id>', methods=['DELETE'])
@token_required
def delete_post(current_user, id):
    global posts
    posts = [post for post in posts if post['id'] != id]
    return jsonify({'message': 'Post deleted successfully!'}), 200

# Running the Flask App
# if __name__ == '__main__':
#     app.run(debug=True)

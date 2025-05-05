import requests

# Base URL for your local Flask app
base_url = 'http://127.0.0.1:5000/' # enter your vercel url

# 1. Sign up a new user (POST request)
def signup():
    url = base_url + 'signup'
    data = {
        'username': 'admin',
        'password': 'adminpass'
    }
    response = requests.post(url, json=data)
    print(f"Signup Response: {response.json()}")

# 2. Login and get JWT token (POST request)
def login():
    url = base_url + 'login'
    data = {
        'username': 'admin',
        'password': 'adminpass'
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"Login Success, Token: {token}")
        return token
    else:
        print("Login failed:", response.json())
        return None

# 3. Create a new post (POST request)
def create_post(token):
    url = base_url + 'post'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'title': 'New Post',
        'content': 'This is the content of the new post.'
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Create Post Response: {response.json()}")

# 4. Get all posts (GET request)
def get_posts(token):
    url = base_url + 'posts'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(f"Get Posts Response: {response.json()}")

# 5. Update post (PUT request)
def update_post(token, post_id):
    url = base_url + f'post/{post_id}'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'title': 'Updated Post Title',
        'content': 'Updated content of the post.'
    }
    response = requests.put(url, json=data, headers=headers)
    print(f"Update Post Response: {response.json()}")

# 6. Delete post (DELETE request)
def delete_post(token, post_id):
    url = base_url + f'post/{post_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(url, headers=headers)
    print(f"Delete Post Response: {response.json()}")

# Main flow
def main():
    # Step 1: Sign up a new user
    signup()

    # Step 2: Log in and get the JWT token
    token = login()

    if token:
        # Step 3: Create a new post using the JWT token
        create_post(token)

        # Step 4: Get all posts using the JWT token
        get_posts(token)

        # Step 5: Update a post using the JWT token (assuming post ID is 1)
        update_post(token, post_id=1)

        # Step 6: Delete a post using the JWT token (assuming post ID is 1)
        delete_post(token, post_id=1)

if __name__ == "__main__":
    main()

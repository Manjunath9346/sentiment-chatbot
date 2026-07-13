import json
import os

DATA_FILE = "user_data.json"

def load_data():
    """Load user data from JSON file. Returns dict."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": {}}

def save_data(data):
    """Save user data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_conversations(username):
    """Return list of conversations for a user, or empty list if new."""
    data = load_data()
    user = data["users"].get(username)
    if user:
        return user.get("conversations", [])
    return []

def save_user_conversations(username, conversations):
    """Save conversations for a specific user."""
    data = load_data()
    if username not in data["users"]:
        data["users"][username] = {"password": "", "conversations": []}
    data["users"][username]["conversations"] = conversations
    save_data(data)

def user_exists(username):
    data = load_data()
    return username in data["users"]

def verify_password(username, password):
    data = load_data()
    user = data["users"].get(username)
    if user and user.get("password") == password:
        return True
    return False

def register_user(username, password):
    data = load_data()
    if username in data["users"]:
        return False  # user already exists
    data["users"][username] = {
        "password": password,
        "conversations": []
    }
    save_data(data)
    return True
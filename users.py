import json
import os
import hashlib
import uuid

# Use absolute path
users_file = os.path.join(os.path.dirname(__file__), "data", "users.json")


def load_users():
    """Load users from JSON file"""
    try:
        if not os.path.exists(users_file):
            # Create empty users file if it doesn't exist
            save_users({})
            return {}
        with open(users_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}
def save_users(users):
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)

def add_user(name: str, password: str, currency: str) -> dict:
    """Create a new user and save to users file"""
    users = load_users()
    if name in users:
        raise ValueError("Username already exists!")
    user_id = str(uuid.uuid4())
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[name] = {
        "id": user_id,
        "name": name,
        "password": hashed_password,
        "currency": currency
    }
    save_users(users)
    return users[name]
def authenticate_user(name: str, password: str) -> dict:
    """Authenticate user by name and password"""
    users = load_users()
    if name not in users:
        return None
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if users[name]["password"] != hashed_password:
        return None
    return users[name]
def create_user(name: str, password: str, currency: str) -> dict:
    """Create a new user and return user data"""
    try:
        user = add_user(name, password, currency)
        return user
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError("Failed to create user") from e
def switch_user(name: str, password: str, current_user: dict) -> dict:
    """Switch to a different user account"""
    user = authenticate_user(name, password)
    if user:
        return user
    else:
        raise ValueError("Invalid username or password")
def change_password(user: dict, old_password: str, new_password: str) -> bool:
    """Change password for the given user"""
    users = load_users()
    if user["name"] not in users:
        raise ValueError("User does not exist")
    hashed_old_password = hashlib.sha256(old_password.encode()).hexdigest()
    if users[user["name"]]["password"] != hashed_old_password:
        raise ValueError("Old password is incorrect")
    hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
    users[user["name"]]["password"] = hashed_new_password
    save_users(users)
    return True
def delete_user(user: dict, confirm: bool = True) -> bool:
    """Delete the given user account"""
    if confirm:
        users = load_users()
        if user["name"] in users:
            del users[user["name"]]
            save_users(users)
            return True
        else:
            raise ValueError("User does not exist")
    else:
        return False
def list_users() -> list:
    """Return a list of all users"""
    users = load_users()
    return [users[name] for name in users]
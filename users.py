
from jsonhandler import JsonHandler as jh
from utility import Utilities as util

class User:
    user_count = 0
    def __init__(self, name, password, currency='USD'):
        self.id = util.generate_uuid()
        self.name = name
        self.password = util.hash_password(password)
        self.currency = currency
        self.__register_user()

    def __register_user(self):
        """Private method to handle saving user data"""
        users = jh.load_users()
        if self.name in users:
            raise ValueError("Username already exists!")

        users[self.name] = {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "currency": self.currency
        }
        jh.save_users(users)
        User.user_count += 1
  
    @staticmethod
    def login(current_user):
        """Login or switch user interactively"""
        name = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        users = jh.load_users()

        if name not in users:
            raise ValueError("Username not found")

        hashed_password = util.hash_password(password)
        if users[name]["password"] != hashed_password:
            raise ValueError("Incorrect password")
        if current_user and current_user["name"] != name:
            print(f"Switched from {current_user['name']} to {name}.")
        else:
            print(f"Login successful. Welcome {name}!")

        return users[name]
        
    
    def change_password(self):
        """Change password for the given user"""
        users = jh.load_users()
        old_password = input("Enter old password: ").strip()
        hashed_old_password = util.hash_password(old_password)
        if users[self.name]["password"] != hashed_old_password:
            raise ValueError("Old password is incorrect")
        new_password = input("Enter new password: ").strip()
        hashed_new_password = util.hash_password(new_password)
        users[self.name]["password"] = hashed_new_password
        jh.save_users(users)
        print("Password changed successfully.")
        return True
    
    def delete_user(self):
        """Delete the given user account"""
        password = input("Enter your password to confirm deletion: ").strip()
        hashed_password = util.hash_password(password)
        users = jh.load_users()
        if users[self.name]["password"] != hashed_password:
            raise ValueError("Password is incorrect")
        del users[self.name]
        jh.save_users(users)
        User.user_count -= 1
        print(f"User {self.name} deleted successfully.")
        return True



    @staticmethod   
    def list_users():
        """Return a list of all users"""
        users = jh.load_users()
        return [users[name] for name in users]
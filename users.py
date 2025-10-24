
from jsonhandler import JsonHandler
from utility import Utilities
from typing import Dict, List, Optional, Any


class User:
    """User class for managing user accounts and authentication"""
    
    user_count = 0
    _json_handler = JsonHandler()
    _utilities = Utilities()
    
    def __init__(self, name: str, password: str, currency: str = 'USD'):
        """Initialize a new user"""
        self.id = self._utilities.generate_uuid()
        self.name = name
        self.password = self._utilities.hash_password(password)
        self.currency = currency
        self._register_user()

    def _register_user(self) -> None:
        """Private method to handle saving user data"""
        users = self._json_handler.load_users()
        if self.name in users:
            raise ValueError("Username already exists!")

        users[self.name] = {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "currency": self.currency
        }
        
        if not self._json_handler.save_users(users):
            raise RuntimeError("Failed to save user data")
        
        User.user_count += 1
  
    @classmethod
    def login(cls, current_user: Optional[Dict] = None) -> Dict[str, Any]:
        """Login or switch user interactively"""
        name = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        users = cls._json_handler.load_users()

        if name not in users:
            raise ValueError("Username not found")

        hashed_password = cls._utilities.hash_password(password)
        if users[name]["password"] != hashed_password:
            raise ValueError("Incorrect password")
        
        if current_user and current_user["name"] != name:
            print(f"Switched from {current_user['name']} to {name}.")
        else:
            print(f"Login successful. Welcome {name}!")

        return users[name]
    
    def change_password(self) -> bool:
        """Change password for the given user"""
        users = self._json_handler.load_users()
        old_password = input("Enter old password: ").strip()
        hashed_old_password = self._utilities.hash_password(old_password)
        
        if users[self.name]["password"] != hashed_old_password:
            raise ValueError("Old password is incorrect")
        
        new_password = input("Enter new password: ").strip()
        if not new_password:
            raise ValueError("New password cannot be empty")
        
        hashed_new_password = self._utilities.hash_password(new_password)
        users[self.name]["password"] = hashed_new_password
        
        if not self._json_handler.save_users(users):
            raise RuntimeError("Failed to save password change")
        
        self.password = hashed_new_password
        print("Password changed successfully.")
        return True
    
    def delete_user(self) -> bool:
        """Delete the given user account"""
        password = input("Enter your password to confirm deletion: ").strip()
        hashed_password = self._utilities.hash_password(password)
        users = self._json_handler.load_users()
        
        if users[self.name]["password"] != hashed_password:
            raise ValueError("Password is incorrect")
        
        del users[self.name]
        
        if not self._json_handler.save_users(users):
            raise RuntimeError("Failed to save user deletion")
        
        User.user_count -= 1
        print(f"User {self.name} deleted successfully.")
        return True

    def update_currency(self, new_currency: str) -> bool:
        """Update user's preferred currency"""
        users = self._json_handler.load_users()
        users[self.name]["currency"] = new_currency
        self.currency = new_currency
        
        if not self._json_handler.save_users(users):
            raise RuntimeError("Failed to save currency update")
        
        print(f"Currency updated to {new_currency}")
        return True

    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information"""
        return {
            "id": self.id,
            "name": self.name,
            "currency": self.currency
        }

    @classmethod
    def list_users(cls) -> List[Dict[str, Any]]:
        """Return a list of all users"""
        users = cls._json_handler.load_users()
        return [users[name] for name in users]
    
    @classmethod
    def get_user_by_name(cls, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users = cls._json_handler.load_users()
        return users.get(username)
    
    @classmethod
    def user_exists(cls, username: str) -> bool:
        """Check if user exists"""
        users = cls._json_handler.load_users()
        return username in users
    
    @classmethod
    def get_user_count(cls) -> int:
        """Get total number of users"""
        users = cls._json_handler.load_users()
        return len(users)
    
    @classmethod
    def show_user_profile(cls, user_id: str) -> None:
        """Display user profile with financial summary"""
        try:
            # Get user information
            users = cls._json_handler.load_users()
            user_info = None
            for username, user_data in users.items():
                if user_data['id'] == user_id:
                    user_info = user_data
                    break
            
            if not user_info:
                print("User not found!")
                return
            
            # Get user's transactions
            from transactions import Transaction
            transactions = Transaction.view_transactions(user_id)
            
            # Calculate financial summary
            total_income = 0.0
            total_expenses = 0.0
            
            for transaction in transactions:
                if transaction['type'] == 'income':
                    total_income += transaction['amount']
                elif transaction['type'] == 'expense':
                    total_expenses += transaction['amount']
            
            net_savings = total_income - total_expenses
            
            # Display profile
            print("\n" + "="*50)
            print("           USER PROFILE")
            print("="*50)
            print(f"Name: {user_info['name']}")
            print(f"Currency: {user_info['currency']}")
            print(f"User ID: {user_info['id']}")
            print("-"*50)
            print("FINANCIAL SUMMARY")
            print("-"*50)
            print(f"Total Income:  {cls._utilities.format_currency(total_income, user_info['currency'])}")
            print(f"Total Expenses: {cls._utilities.format_currency(total_expenses, user_info['currency'])}")
            print(f"Net Savings:   {cls._utilities.format_currency(net_savings, user_info['currency'])}")
            print("-"*50)
            print(f"Total Transactions: {len(transactions)}")
            print("="*50)
            
        except Exception as e:
            print(f"Error displaying user profile: {e}")
    
    @classmethod
    def get_financial_summary(cls, user_id: str) -> Dict[str, Any]:
        """Get financial summary data for a user"""
        try:
            # Get user information
            users = cls._json_handler.load_users()
            user_info = None
            for username, user_data in users.items():
                if user_data['id'] == user_id:
                    user_info = user_data
                    break
            
            if not user_info:
                return {"error": "User not found"}
            
            # Get user's transactions
            from transactions import Transaction
            transactions = Transaction.view_transactions(user_id)
            
            # Calculate financial summary
            total_income = 0.0
            total_expenses = 0.0
            income_transactions = 0
            expense_transactions = 0
            
            for transaction in transactions:
                if transaction['type'] == 'income':
                    total_income += transaction['amount']
                    income_transactions += 1
                elif transaction['type'] == 'expense':
                    total_expenses += transaction['amount']
                    expense_transactions += 1
            
            net_savings = total_income - total_expenses
            
            return {
                "user_info": user_info,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net_savings": net_savings,
                "total_transactions": len(transactions),
                "income_transactions": income_transactions,
                "expense_transactions": expense_transactions,
                "currency": user_info['currency']
            }
            
        except Exception as e:
            return {"error": f"Error getting financial summary: {e}"}
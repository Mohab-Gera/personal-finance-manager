import os
import json
from typing import Dict, Any, Optional


class JsonHandler:
    """Singleton class for handling JSON file operations"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JsonHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.users_file = os.path.join(os.path.dirname(__file__), "data", "users.json")
            self.transactions_file = os.path.join(os.path.dirname(__file__), "data", "transactions.json")
            self.bills_file = os.path.join(os.path.dirname(__file__), "data", "bills.json")
            self._ensure_data_directory()
            self._initialized = True
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists"""
        data_dir = os.path.dirname(self.users_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def load_users(self) -> Dict[str, Any]:
        """Load users from JSON file"""
        try:
            if not os.path.exists(self.users_file):
                # Create empty users file if it doesn't exist
                self.save_users({})
                return {}
            with open(self.users_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    
    def save_users(self, users: Dict[str, Any]) -> bool:
        """Save users to JSON file"""
        try:
            with open(self.users_file, "w") as f:
                json.dump(users, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def load_transactions(self) -> Dict[str, Any]:
        """Load transactions from JSON file"""
        try:
            if not os.path.exists(self.transactions_file):
                # Initialize with empty dict for first use
                self.save_transactions({})
                return {}
            
            with open(self.transactions_file, 'r') as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return {}

    def save_transactions(self, transactions: Dict[str, Any]) -> bool:
        """Save transactions to JSON file"""
        try:
            with open(self.transactions_file, 'w') as f:
                json.dump(transactions, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving transactions: {e}")
            return False
    
    def backup_data(self, backup_dir: str = None) -> bool:
        """Create backup of all data files"""
        try:
            if backup_dir is None:
                backup_dir = os.path.join(os.path.dirname(__file__), "data", "backup")
            
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            import shutil
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup users
            if os.path.exists(self.users_file):
                shutil.copy2(self.users_file, os.path.join(backup_dir, f"users_{timestamp}.json"))
            
            # Backup transactions
            if os.path.exists(self.transactions_file):
                shutil.copy2(self.transactions_file, os.path.join(backup_dir, f"transactions_{timestamp}.json"))
            
            # Backup bills
            if os.path.exists(self.bills_file):
                shutil.copy2(self.bills_file, os.path.join(backup_dir, f"bills_{timestamp}.json"))
            
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def load_bills(self) -> Dict[str, Any]:
        """Load bills from JSON file"""
        try:
            if not os.path.exists(self.bills_file):
                # Create empty bills file if it doesn't exist
                self.save_bills({})
                return {}
            
            with open(self.bills_file, 'r') as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except Exception as e:
            print(f"Error loading bills: {e}")
            return {}
    
    def save_bills(self, bills: Dict[str, Any]) -> bool:
        """Save bills to JSON file"""
        try:
            with open(self.bills_file, 'w') as f:
                json.dump(bills, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving bills: {e}")
            return False

import os
import json

class JsonHandler:


    users_file = os.path.join(os.path.dirname(__file__), "data", "users.json")
    transations_file = os.path.join(os.path.dirname(__file__), "data", "transactions.json")

    #Load users from JSON file
    @staticmethod
    def load_users():
        try:
            if not os.path.exists(JsonHandler.users_file):
                # Create empty users file if it doesn't exist
                JsonHandler.save_users({})
                return {}
            with open(JsonHandler.users_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    @staticmethod
    def save_users(users):
        with open(JsonHandler.users_file, "w") as f:
            json.dump(users, f, indent=4)
    
    @staticmethod
    def load_transactions():
        # Load transactions from JSON file
        try:
            with open(JsonHandler.transations_file, 'r') as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except FileNotFoundError:
            # Initialize with empty dict for first use
            with open(JsonHandler.transations_file, 'w') as f:
                json.dump({}, f)
            return {}
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return {}

    @staticmethod
    def save_transactions(transactions):
        # Save transactions to JSON file
        try:
            with open(JsonHandler.transations_file, 'w') as f:
                json.dump(transactions, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving transactions: {e}")
            return False

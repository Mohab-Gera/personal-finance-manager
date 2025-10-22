from typing import Dict, List
import json
import os
from datetime import datetime
from utilities import validate_amount, validate_date, generate_transaction_id

# Constants
TRANSACTIONS_FILE = os.path.join(os.path.dirname(__file__), "data", "transactions.json")
CATEGORIES = {
    "expense": ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"],
    "income": ["Salary", "Freelance", "Investment", "Gift", "Other"]
}
PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "Bank Transfer"]

def transactions_menu(current_user):
    while True:
        print("\n------ Transactions Menu ------")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Back to Main Menu")
        print("-------------------------------")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            try:
                print("\nAdding new transaction...")
                t_type = input("Transaction type (expense/income): ").lower()
                amount = input("Amount: ")
                category = input(f"Category {CATEGORIES[t_type]}: ")
                date = input("Date (YYYY-MM-DD) or press enter for today: ")
                description = input("Description: ")
                payment_method = input(f"Payment method {PAYMENT_METHODS}: ")
                
                transaction = add_transaction(
                    current_user['id'],
                    type=t_type,
                    amount=amount,
                    category=category,
                    date=date or None,
                    description=description,
                    payment_method=payment_method
                )
                
                if transaction:
                    print("\nTransaction added successfully!")
                
            except Exception as e:
                print(f"\nError: {e}")
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            print("\nViewing all transactions...")
            transactions = view_transactions(current_user['id'])
            if transactions:
                print(f"\n--- Your Transactions ({len(transactions)}) ---")
                for idx, t in enumerate(transactions, 1):
                    print(f"\n[{idx}] {t['date']} - {t['type'].upper()}")
                    print(f"    Amount: {t['amount']} | Category: {t['category']}")
                    print(f"    Description: {t['description']}")
                    print(f"    Payment Method: {t['payment_method']}")
                    print("-" * 40)
            else:
                print("\nNo transactions found.")
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            print("\nEditing transaction...")
            selected = select_transaction(current_user['id'], "edit")
            
            if selected:
                # Store accumulated changes
                new_values = {}
                
                while True:
                    print("\nCurrent Transaction Values:")
                    print(f"1. Type: {selected['type']}")
                    print(f"2. Amount: {selected['amount']}")
                    print(f"3. Category: {selected['category']}")
                    print(f"4. Date: {selected['date']}")
                    print(f"5. Description: {selected['description']}")
                    print(f"6. Payment Method: {selected['payment_method']}")
                    print("7. Save and Exit")
                    print("8. Cancel")
                    print("-" * 40)
                    
                    edit_choice = input("\nEnter your choice (1-8): ").strip()
                    
                    if edit_choice == "1":
                        print(f"Current type: {selected['type']}")
                        new_type = input("New transaction type (expense/income): ").lower()
                        if new_type in ['expense', 'income']:
                            new_values['type'] = new_type
                            selected['type'] = new_type
                            print("Type updated!")
                        else:
                            print("Invalid type! Must be 'expense' or 'income'")
                            
                    elif edit_choice == "2":
                        print(f"Current amount: {selected['amount']}")
                        new_amount = input("New amount: ")
                        if validate_amount(new_amount):
                            new_values['amount'] = float(new_amount)
                            selected['amount'] = float(new_amount)
                            print("Amount updated!")
                        else:
                            print("Invalid amount!")
                            
                    elif edit_choice == "3":
                        t_type = selected['type']
                        print(f"Current category: {selected['category']}")
                        print(f"Available categories for {t_type}: {CATEGORIES[t_type]}")
                        new_category = input("New category: ")
                        if new_category in CATEGORIES[t_type]:
                            new_values['category'] = new_category
                            selected['category'] = new_category
                            print("Category updated!")
                        else:
                            print("Invalid category!")
                            
                    elif edit_choice == "4":
                        print(f"Current date: {selected['date']}")
                        new_date = input("New date (YYYY-MM-DD): ")
                        if validate_date(new_date):
                            new_values['date'] = new_date
                            selected['date'] = new_date
                            print("Date updated!")
                        else:
                            print("Invalid date format!")
                            
                    elif edit_choice == "5":
                        print(f"Current description: {selected['description']}")
                        new_desc = input("New description: ")
                        if new_desc.strip():
                            new_values['description'] = new_desc
                            selected['description'] = new_desc
                            print("Description updated!")
                        else:
                            print("Description cannot be empty!")
                            
                    elif edit_choice == "6":
                        print(f"Current payment method: {selected['payment_method']}")
                        print(f"Available methods: {PAYMENT_METHODS}")
                        new_method = input("New payment method: ")
                        if new_method in PAYMENT_METHODS:
                            new_values['payment_method'] = new_method
                            selected['payment_method'] = new_method
                            print("Payment method updated!")
                        else:
                            print("Invalid payment method!")
                            
                    elif edit_choice == "7":
                        if new_values:
                            if edit_transaction(selected['transaction_id'], new_values):
                                print("\nTransaction updated successfully!")
                            else:
                                print("\nFailed to update transaction!")
                        else:
                            print("\nNo changes made to transaction.")
                        break
                        
                    elif edit_choice == "8":
                        print("\nEdit cancelled.")
                        break
                        
                    else:
                        print("\nInvalid choice! Please try again.")
            
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            print("\nDeleting transaction...")
            selected = select_transaction(current_user['id'], "delete")
            
            if selected:
                if delete_transaction(selected['transaction_id']):
                    print("\nTransaction deleted successfully!")
                else:
                    print("\nFailed to delete transaction or cancelled.")
            
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            print("\nReturning to Main Menu...")
            break
            
        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")
            input("\nPress Enter to continue...")


def load_transactions() -> Dict:
    """Load transactions from JSON file"""
    try:
        with open(TRANSACTIONS_FILE, 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except FileNotFoundError:
        # Initialize with empty dict for first use
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump({}, f)
        return {}
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return {}


def save_transactions(transactions: Dict) -> bool:
    """Save transactions to JSON file"""
    try:
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump(transactions, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving transactions: {e}")
        return False


def add_transaction(user_id: str, **kwargs) -> Dict:
    """Add a new transaction"""
    try:
        # Load existing transactions
        transactions = load_transactions()
        
        # Validate date
        date = kwargs.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        elif not validate_date(date):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
            
        # Create transaction
        transaction = {
            "transaction_id": generate_transaction_id(),
            "user_id": user_id,
            "type": kwargs.get('type'),
            "amount": float(kwargs.get('amount')),
            "category": kwargs.get('category'),
            "date": date,
            "description": kwargs.get('description', ''),
            "payment_method": kwargs.get('payment_method')
        }
        
        # Add to transactions
        if user_id not in transactions:
            transactions[user_id] = []
        transactions[user_id].append(transaction)
        
        # Save and return
        if save_transactions(transactions):
            return transaction
        raise RuntimeError("Failed to save transaction")
        
    except ValueError as e:
        print(f"Error adding transaction: {str(e)}")
        return None
    except Exception as e:
        print(f"Error adding transaction: {str(e)}")
        return None

    
def select_transaction(user_id: str, action: str = "select") -> Dict:
    """Display transactions in a numbered list and let user select one"""
    transactions = view_transactions(user_id)
    if not transactions:
        print("\nNo transactions found.")
        return None
        
    print(f"\n--- Your Transactions ({len(transactions)}) ---")
    for idx, t in enumerate(transactions, 1):
        print(f"\n[{idx}] {t['date']} - {t['type'].upper()}")
        print(f"    Amount: {t['amount']} | Category: {t['category']}")
        print(f"    Description: {t['description']}")
        print(f"    Payment Method: {t['payment_method']}")
        print("-" * 40)
    
    try:
        choice = input(f"\nEnter number (1-{len(transactions)}) to {action}, or 0 to cancel: ")
        if not choice.isdigit():
            print("Please enter a number.")
            return None
            
        choice = int(choice)
        if choice == 0:
            return None
        if choice < 1 or choice > len(transactions):
            print("Invalid selection.")
            return None
            
        return transactions[choice - 1]
    except Exception as e:
        print(f"Error selecting transaction: {e}")
        return None


def view_transactions(user_id: str) -> List[Dict]:
    """View all transactions for a user"""
    try:
        transactions = load_transactions()
        return transactions.get(user_id, [])
    except Exception as e:
        print(f"Error viewing transactions: {e}")
        return []


def get_transaction_by_id(transaction_id: str) -> Dict:
    """Get a specific transaction by ID"""
    try:
        transactions = load_transactions()
        for user_transactions in transactions.values():
            for transaction in user_transactions:
                if transaction['transaction_id'] == transaction_id:
                    return transaction
        return None
    except Exception as e:
        print(f"Error getting transaction: {e}")
        return None


def edit_transaction(transaction_id: str, new_values: Dict) -> bool:
    """Edit an existing transaction"""
    try:
        transactions = load_transactions()
        modified = False
        
        # Find and update transaction
        for user_id, user_transactions in transactions.items():
            for i, transaction in enumerate(user_transactions):
                if transaction['transaction_id'] == transaction_id:
                    # Update only valid fields
                    for key, value in new_values.items():
                        if key in transaction and key != 'transaction_id' and key != 'user_id':
                            transaction[key] = value
                            modified = True
                    
                    if modified:
                        transactions[user_id][i] = transaction
                        return save_transactions(transactions)
        
        if not modified:
            print("Transaction not found or no valid changes to make")
            return False
        
        return False
        
    except Exception as e:
        print(f"Error editing transaction: {e}")
        return False


def delete_transaction(transaction_id: str, confirm: bool = True) -> bool:
    """Delete a transaction"""
    try:
        if confirm:
            confirmation = input("Are you sure you want to delete this transaction? (y/n): ")
            if confirmation.lower() != 'y':
                return False
                
        transactions = load_transactions()
        
        # Find and delete transaction
        for user_id, user_transactions in transactions.items():
            for transaction in user_transactions:
                if transaction['transaction_id'] == transaction_id:
                    transactions[user_id].remove(transaction)
                    return save_transactions(transactions)
                    
        raise ValueError("Transaction not found")
        
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False
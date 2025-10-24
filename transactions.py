from jsonhandler import JsonHandler
from utility import Utilities
from datetime import datetime
from typing import Dict, List, Optional, Any


class TransactionManager:
    """Manager class for handling transaction operations"""
    
    CATEGORIES = {
        "expense": ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"],
        "income": ["Salary", "Freelance", "Investment", "Gift", "Other"]
    }
    PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "Bank Transfer"]
    
    def __init__(self):
        self._json_handler = JsonHandler()
        self._utilities = Utilities()
    
    def add_transaction(self, user_id: str, type: str, amount: str, category: str, 
                       date: Optional[str] = None, description: str = "", 
                       payment_method: str = "") -> Optional[Dict[str, Any]]:
        """Add a new transaction"""
        try:
            # Normalize inputs
            type = type.lower().strip()
            category = self._normalize_category(category, type)
            payment_method = self._normalize_payment_method(payment_method)
            
            # Validate inputs
            if not self._utilities.validate_amount(amount):
                raise ValueError("Invalid amount")
            
            if type not in self.CATEGORIES:
                raise ValueError("Invalid transaction type")
            
            if category not in self.CATEGORIES[type]:
                raise ValueError("Invalid category for transaction type")
            
            if payment_method not in self.PAYMENT_METHODS:
                raise ValueError("Invalid payment method")
            
            # Create transaction object
            transaction = Transaction(
                user_id=user_id,
                type=type,
                amount=float(amount),
                category=category,
                date=date,
                description=description,
                payment_method=payment_method
            )
            
            return transaction.add_transaction()
            
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None
    
    def view_transactions(self, user_id: str) -> List[Dict[str, Any]]:
        """View all transactions for a user"""
        return Transaction.view_transactions(user_id)
    
    def edit_transaction(self, transaction_id: str, new_values: Dict[str, Any]) -> bool:
        """Edit an existing transaction"""
        result = Transaction.edit_transaction(transaction_id, new_values)
        return result.get("success", False)
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction"""
        result = Transaction.delete_transaction(transaction_id)
        return result.get("success", False)
    
    def select_transaction(self, user_id: str, action: str = "select") -> Optional[Dict[str, Any]]:
        """Select a transaction for editing/deleting"""
        return Transaction.select_transaction(user_id, action)
    
    def get_categories(self, transaction_type: str) -> List[str]:
        """Get available categories for transaction type"""
        return self.CATEGORIES.get(transaction_type, [])
    
    def get_payment_methods(self) -> List[str]:
        """Get available payment methods"""
        return self.PAYMENT_METHODS.copy()
    
    def _normalize_category(self, category: str, transaction_type: str) -> str:
        """Normalize category input to match the correct case from predefined categories"""
        if not category:
            return category
        
        available_categories = self.get_categories(transaction_type)
        category_lower = category.lower()
        
        # Find matching category (case-insensitive)
        for valid_category in available_categories:
            if valid_category.lower() == category_lower:
                return valid_category
        
        # If no exact match found, return original input
        return category
    
    def _normalize_payment_method(self, payment_method: str) -> str:
        """Normalize payment method input to match the correct case from predefined methods"""
        if not payment_method:
            return payment_method
        
        payment_method_lower = payment_method.lower()
        
        # Find matching payment method (case-insensitive)
        for valid_method in self.PAYMENT_METHODS:
            if valid_method.lower() == payment_method_lower:
                return valid_method
        
        # If no exact match found, return original input
        return payment_method

def transactions_menu(current_user: Dict[str, Any]) -> None:
    """Transaction menu interface"""
    manager = TransactionManager()
    utilities = Utilities()
    
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
                t_type = input("Transaction type (expense/income): ").lower().strip()
                amount = input("Amount: ")
                category = input(f"Category {manager.get_categories(t_type)}: ").strip()
                date = input("Date (YYYY-MM-DD) or press enter for today: ").strip()
                description = input("Description: ").strip()
                payment_method = input(f"Payment method {manager.get_payment_methods()}: ").strip()
                
                # Normalize category and payment method to match case-insensitive
                category = manager._normalize_category(category, t_type)
                payment_method = manager._normalize_payment_method(payment_method)
                
                transaction = manager.add_transaction(
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
            utilities.pause()
            
        elif choice == "2":
            print("\nViewing all transactions...")
            transactions = manager.view_transactions(current_user['id'])
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
            utilities.pause()
            
        elif choice == "3":
            print("\nEditing transaction...")
            selected = manager.select_transaction(current_user['id'], "edit")
            
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
                        new_type = input("New transaction type (expense/income): ").lower().strip()
                        if new_type in ['expense', 'income']:
                            new_values['type'] = new_type
                            selected['type'] = new_type
                            print("Type updated!")
                        else:
                            print("Invalid type! Must be 'expense' or 'income'")
                            
                    elif edit_choice == "2":
                        print(f"Current amount: {selected['amount']}")
                        new_amount = input("New amount: ")
                        if utilities.validate_amount(new_amount):
                            new_values['amount'] = float(new_amount)
                            selected['amount'] = float(new_amount)
                            print("Amount updated!")
                        else:
                            print("Invalid amount!")
                            
                    elif edit_choice == "3":
                        t_type = selected['type']
                        print(f"Current category: {selected['category']}")
                        print(f"Available categories for {t_type}: {manager.get_categories(t_type)}")
                        new_category = input("New category: ").strip()
                        # Normalize the category input
                        normalized_category = manager._normalize_category(new_category, t_type)
                        if normalized_category in manager.get_categories(t_type):
                            new_values['category'] = normalized_category
                            selected['category'] = normalized_category
                            print("Category updated!")
                        else:
                            print("Invalid category!")
                            
                    elif edit_choice == "4":
                        print(f"Current date: {selected['date']}")
                        new_date = input("New date (YYYY-MM-DD): ")
                        if utilities.validate_date(new_date):
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
                        print(f"Available methods: {manager.get_payment_methods()}")
                        new_method = input("New payment method: ").strip()
                        # Normalize the payment method input
                        normalized_method = manager._normalize_payment_method(new_method)
                        if normalized_method in manager.get_payment_methods():
                            new_values['payment_method'] = normalized_method
                            selected['payment_method'] = normalized_method
                            print("Payment method updated!")
                        else:
                            print("Invalid payment method!")
                            
                    elif edit_choice == "7":
                        if new_values:
                            if manager.edit_transaction(selected['transaction_id'], new_values):
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
            
            utilities.pause()
            
        elif choice == "4":
            print("\nDeleting transaction...")
            selected = manager.select_transaction(current_user['id'], "delete")
            
            if selected:
                if manager.delete_transaction(selected['transaction_id']):
                    print("\nTransaction deleted successfully!")
                else:
                    print("\nFailed to delete transaction or cancelled.")
            
            utilities.pause()
            
        elif choice == "5":
            print("\nReturning to Main Menu...")
            break
            
        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")
            utilities.pause()

class Transaction:
    """Transaction class representing a single financial transaction"""
    
    transaction_count = 0
    _json_handler = JsonHandler()
    _utilities = Utilities()
    
    def __init__(self, user_id: str, type: str, amount: float, category: str, 
                 date: Optional[str] = None, description: str = "", 
                 payment_method: str = ""):
        """Initialize a new transaction"""
        self.user_id = user_id
        self.transaction_id = self._utilities.generate_uuid()
        self.type = type
        self.amount = amount
        self.category = category
        self.date = self._validate_date(date)
        self.description = description
        self.payment_method = payment_method
        Transaction.transaction_count += 1

    def _validate_date(self, date: Optional[str]) -> str:
        """Private method to validate and format date"""
        if not date:
            return self._utilities.get_current_date()
        
        if self._utilities.validate_date(date):
            if self._utilities.is_future_date(date):
                raise ValueError("Date cannot be in the future")
            return date
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
    def add_transaction(self) -> Optional[Dict[str, Any]]:
        """Add this transaction to storage (JSON)"""
        try:
            transactions = self._json_handler.load_transactions()

            transaction = {
                "transaction_id": self.transaction_id,
                "user_id": self.user_id,
                "type": self.type,
                "amount": float(self.amount),
                "category": self.category,
                "date": self.date,  
                "description": self.description,
                "payment_method": self.payment_method
            }
            
            if self.user_id not in transactions:
                transactions[self.user_id] = []
            transactions[self.user_id].append(transaction)
            
            if self._json_handler.save_transactions(transactions):
                return transaction
            raise RuntimeError("Failed to save transaction")

        except ValueError as e:
            print(f"Error adding transaction: {str(e)}")
            return None
        except Exception as e:
            print(f"Error adding transaction: {str(e)}")
            return None

    @classmethod
    def view_transactions(cls, user_id: str) -> List[Dict[str, Any]]:
        """View all transactions for a user
        
        Args:
            user_id: The user's ID
            
        Returns:
            List of transaction dictionaries
        """
        try:
            transactions = cls._json_handler.load_transactions()
            return transactions.get(user_id, [])
        except Exception as e:
            print(f"Error viewing transactions: {e}")
            return []

    @classmethod
    def get_transaction_by_id(cls, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific transaction by ID
        
        Args:
            transaction_id: The transaction's unique ID
            
        Returns:
            Transaction dictionary or None if not found
        """
        try:
            transactions = cls._json_handler.load_transactions()
            for user_transactions in transactions.values():
                for transaction in user_transactions:
                    if transaction['transaction_id'] == transaction_id:
                        return transaction
            return None
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None

    @classmethod
    def edit_transaction(cls, transaction_id: str, new_values: Dict[str, Any]) -> Dict[str, Any]:
        """Edit an existing transaction
        
        Args:
            transaction_id: The transaction's unique ID
            new_values: Dictionary with fields to update
            
        Returns:
            Dict with success status and message/data
        """
        try:
            transactions = cls._json_handler.load_transactions()
            
            # Allowed fields to edit
            allowed_fields = {'type', 'amount', 'category', 'date', 'description', 'payment_method'}
            
            for user_id, user_transactions in transactions.items():
                for i, transaction in enumerate(user_transactions):
                    if transaction['transaction_id'] == transaction_id:
                        # Validate and update fields
                        updated_fields = {}
                        for key, value in new_values.items():
                            if key in allowed_fields:
                                # Validate date if updating
                                if key == 'date':
                                    if cls._utilities.validate_date(value):
                                        if cls._utilities.is_future_date(value):
                                            return {
                                                "success": False,
                                                "message": "Date cannot be in the future"
                                            }
                                        transaction[key] = value
                                        updated_fields[key] = value
                                    else:
                                        return {
                                            "success": False,
                                            "message": f"Invalid date format for {key}"
                                        }
                                elif key == 'amount':
                                    transaction[key] = float(value)
                                    updated_fields[key] = float(value)
                                else:
                                    transaction[key] = value
                                    updated_fields[key] = value
                        
                        if not updated_fields:
                            return {
                                "success": False,
                                "message": "No valid fields to update"
                            }
                        
                        transactions[user_id][i] = transaction
                        if cls._json_handler.save_transactions(transactions):
                            return {
                                "success": True,
                                "message": "Transaction updated successfully",
                                "data": transaction
                            }
                        return {
                            "success": False,
                            "message": "Failed to save transaction"
                        }
            
            return {
                "success": False,
                "message": "Transaction not found"
            }
            
        except ValueError as e:
            return {
                "success": False,
                "message": f"Validation error: {str(e)}"
            }
        except Exception as e:
            print(f"Error editing transaction: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    @classmethod
    def delete_transaction(cls, transaction_id: str) -> Dict[str, Any]:
        """Delete a transaction
        
        Args:
            transaction_id: The transaction's unique ID
            
        Returns:
            Dict with success status and message
        """
        try:
            transactions = cls._json_handler.load_transactions()
            
            for user_id, user_transactions in transactions.items():
                for transaction in user_transactions:
                    if transaction['transaction_id'] == transaction_id:
                        transactions[user_id].remove(transaction)
                        if cls._json_handler.save_transactions(transactions):
                            return {
                                "success": True,
                                "message": "Transaction deleted successfully",
                                "data": {"transaction_id": transaction_id}
                            }
                        return {
                            "success": False,
                            "message": "Failed to save changes"
                        }
            
            return {
                "success": False,
                "message": "Transaction not found"
            }
            
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    @classmethod
    def select_transaction(cls, user_id: str, action: str = "select") -> Optional[Dict[str, Any]]:
        """Display transactions in a numbered list and let user select one
        (For CLI usage - not typically used in API endpoints)
        
        Args:
            user_id: The user's ID
            action: Action description for display
            
        Returns:
            Selected transaction dictionary or None
        """
        transactions = cls.view_transactions(user_id)
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
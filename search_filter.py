from typing import List, Dict
from datetime import datetime
from transactions import TransactionManager

class SearchFilterManager:
    """
    This class handles all search and filter functionality for the Personal Finance Manager.
    It uses Object-Oriented Programming to organize the search features.
    """
    
    def __init__(self, user_id: str):
        """
        Initialize the SearchFilterManager with a user ID
        This sets up the search workspace for a specific user
        """
        self.user_id = user_id
        self.transactions = self._load_user_transactions()
    
    def _load_user_transactions(self) -> List[Dict]:
        """
        Load all transactions for this user
        This is a helper method that other methods use
        """
        try:
            # Use the TransactionManager to get user's transactions
            tm = TransactionManager()
            return tm.view_transactions(self.user_id)
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
    
    def search_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Search transactions by date range
        This helps you find transactions between two dates
        """
        try:
            # Convert string dates to datetime objects for comparison
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Filter transactions within the date range
            filtered_transactions = []
            for transaction in self.transactions:
                trans_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
                if start_dt <= trans_date <= end_dt:
                    filtered_transactions.append(transaction)
            
            return filtered_transactions
            
        except ValueError as e:
            print(f"Invalid date format. Use YYYY-MM-DD: {e}")
            return []
        except Exception as e:
            print(f"Error searching by date range: {e}")
            return []
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """
        Filter transactions by category
        This helps you find all transactions in a specific category
        """
        try:
            filtered_transactions = []
            for transaction in self.transactions:
                if transaction['category'].lower() == category.lower():
                    filtered_transactions.append(transaction)
            
            return filtered_transactions
            
        except Exception as e:
            print(f"Error filtering by category: {e}")
            return []
    
    def filter_by_amount_range(self, min_amount: float, max_amount: float) -> List[Dict]:
        """
        Filter transactions by amount range
        This helps you find transactions within a specific amount range
        """
        try:
            filtered_transactions = []
            for transaction in self.transactions:
                amount = float(transaction['amount'])
                if min_amount <= amount <= max_amount:
                    filtered_transactions.append(transaction)
            
            return filtered_transactions
            
        except Exception as e:
            print(f"Error filtering by amount range: {e}")
            return []
    
    def sort_transactions(self, transactions_list: List[Dict], key: str = 'amount', reverse: bool = False) -> List[Dict]:
        """
        Sort transactions by specified key
        This helps you organize transactions in different ways
        """
        try:
            if key == 'amount':
                # Sort by amount (convert to float for proper sorting)
                return sorted(transactions_list, key=lambda x: float(x['amount']), reverse=reverse)
            elif key == 'date':
                # Sort by date
                return sorted(transactions_list, key=lambda x: x['date'], reverse=reverse)
            elif key == 'category':
                # Sort by category
                return sorted(transactions_list, key=lambda x: x['category'], reverse=reverse)
            elif key == 'type':
                # Sort by type (income/expense)
                return sorted(transactions_list, key=lambda x: x['type'], reverse=reverse)
            else:
                print(f"Invalid sort key: {key}")
                return transactions_list
                
        except Exception as e:
            print(f"Error sorting transactions: {e}")
            return transactions_list
    
    def display_transactions(self, transactions_list: List[Dict], title: str = "Search Results"):
        """
        Display a list of transactions in a nice format
        This makes the search results easy to read
        """
        if not transactions_list:
            print(f"\n❌ No transactions found for {title}")
            return
        
        print(f"\n" + "="*60)
        print(f"        🔍 {title.upper()}")
        print("="*60)
        print(f"Found {len(transactions_list)} transaction(s)")
        print("-" * 60)
        
        for i, transaction in enumerate(transactions_list, 1):
            trans_type = "💰" if transaction['type'] == 'income' else "💸"
            print(f"\n[{i}] {trans_type} {transaction['date']} - {transaction['type'].upper()}")
            print(f"    Amount: ${transaction['amount']} | Category: {transaction['category']}")
            print(f"    Description: {transaction['description']}")
            print(f"    Payment Method: {transaction['payment_method']}")
            print("-" * 40)
    
    def get_available_categories(self) -> List[str]:
        """
        Get all unique categories from user's transactions
        This helps users see what categories are available
        """
        categories = set()
        for transaction in self.transactions:
            categories.add(transaction['category'])
        return sorted(list(categories))

def search_menu(current_user: Dict) -> None:
    """
    Main search and filter menu - this is the entry point for all search features
    """
    while True:
        print("\n------ Search & Filter Menu ------")
        print("1. Search by Date Range")
        print("2. Filter by Category")
        print("3. Filter by Amount Range")
        print("4. Sort Transactions")
        print("5. View All Transactions")
        print("6. Back to Main Menu")
        print("----------------------------------")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        # Create a SearchFilterManager instance for this user
        search_manager = SearchFilterManager(current_user['id'])
        
        if choice == "1":
            print("\n--- Search by Date Range ---")
            try:
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                
                if start_date and end_date:
                    results = search_manager.search_by_date_range(start_date, end_date)
                    search_manager.display_transactions(results, f"Transactions from {start_date} to {end_date}")
                else:
                    print("Please enter both start and end dates!")
            except Exception as e:
                print(f"Error: {e}")
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            print("\n--- Filter by Category ---")
            # Show available categories
            categories = search_manager.get_available_categories()
            if categories:
                print(f"Available categories: {', '.join(categories)}")
                category = input("Enter category name: ").strip()
                if category:
                    results = search_manager.filter_by_category(category)
                    search_manager.display_transactions(results, f"Transactions in '{category}' category")
                else:
                    print("Please enter a category name!")
            else:
                print("No transactions found to show categories.")
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            print("\n--- Filter by Amount Range ---")
            try:
                min_amount = float(input("Enter minimum amount: "))
                max_amount = float(input("Enter maximum amount: "))
                
                if min_amount <= max_amount:
                    results = search_manager.filter_by_amount_range(min_amount, max_amount)
                    search_manager.display_transactions(results, f"Transactions between ${min_amount} and ${max_amount}")
                else:
                    print("Minimum amount should be less than or equal to maximum amount!")
            except ValueError:
                print("Please enter valid numbers!")
            except Exception as e:
                print(f"Error: {e}")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            print("\n--- Sort Transactions ---")
            print("Sort by:")
            print("1. Amount (Low to High)")
            print("2. Amount (High to Low)")
            print("3. Date (Oldest First)")
            print("4. Date (Newest First)")
            print("5. Category (A-Z)")
            print("6. Type (Income first)")
            
            sort_choice = input("Enter your choice (1-6): ").strip()
            
            if sort_choice == "1":
                results = search_manager.sort_transactions(search_manager.transactions, 'amount', False)
                search_manager.display_transactions(results, "Transactions sorted by Amount (Low to High)")
            elif sort_choice == "2":
                results = search_manager.sort_transactions(search_manager.transactions, 'amount', True)
                search_manager.display_transactions(results, "Transactions sorted by Amount (High to Low)")
            elif sort_choice == "3":
                results = search_manager.sort_transactions(search_manager.transactions, 'date', False)
                search_manager.display_transactions(results, "Transactions sorted by Date (Oldest First)")
            elif sort_choice == "4":
                results = search_manager.sort_transactions(search_manager.transactions, 'date', True)
                search_manager.display_transactions(results, "Transactions sorted by Date (Newest First)")
            elif sort_choice == "5":
                results = search_manager.sort_transactions(search_manager.transactions, 'category', False)
                search_manager.display_transactions(results, "Transactions sorted by Category (A-Z)")
            elif sort_choice == "6":
                results = search_manager.sort_transactions(search_manager.transactions, 'type', False)
                search_manager.display_transactions(results, "Transactions sorted by Type (Income first)")
            else:
                print("Invalid choice!")
            
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            print("\n--- View All Transactions ---")
            search_manager.display_transactions(search_manager.transactions, "All Transactions")
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            break
            
        else:
            print("Invalid choice! Please enter 1-6.")
            input("\nPress Enter to continue...")
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from jsonhandler import JsonHandler
from utility import Utilities
from transactions import TransactionManager

class BudgetTracker:
    """Handles monthly budget tracking and management"""
    
    def __init__(self, user_id: str):
        """Initialize budget tracker for a user"""
        self.user_id = user_id
        self._json_handler = JsonHandler()
        self._utilities = Utilities()
        self._transaction_manager = TransactionManager()
    
    def set_monthly_budget(self, category: str, amount: float, month: str = None) -> bool:
        """Set monthly budget for a specific category"""
        try:
            if not month:
                month = datetime.now().strftime('%Y-%m')
            
            budgets = self._load_budgets()
            if self.user_id not in budgets:
                budgets[self.user_id] = {}
            
            if month not in budgets[self.user_id]:
                budgets[self.user_id][month] = {}
            
            budgets[self.user_id][month][category] = amount
            
            return self._json_handler.save_budgets(budgets)
        except Exception as e:
            print(f"Error setting budget: {e}")
            return False
    
    def get_budget_status(self, month: str = None) -> Dict[str, Any]:
        """Get current budget status for the month"""
        try:
            if not month:
                month = datetime.now().strftime('%Y-%m')
            
            budgets = self._load_budgets()
            user_budgets = budgets.get(self.user_id, {}).get(month, {})
            
            if not user_budgets:
                return {"message": "No budgets set for this month"}
            
            # Get actual spending from transactions
            transactions = self._transaction_manager.view_transactions(self.user_id)
            month_transactions = [t for t in transactions if t['date'].startswith(month)]
            
            status = {}
            for category, budget_amount in user_budgets.items():
                spent = sum(float(t['amount']) for t in month_transactions 
                           if t['category'] == category and t['type'] == 'expense')
                
                remaining = budget_amount - spent
                percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
                
                status[category] = {
                    'budget': budget_amount,
                    'spent': spent,
                    'remaining': remaining,
                    'percentage': percentage
                }
            
            return status
        except Exception as e:
            print(f"Error getting budget status: {e}")
            return {}
    
    def _load_budgets(self) -> Dict[str, Any]:
        """Load budgets from storage"""
        try:
            return self._json_handler.load_budgets()
        except Exception as e:
            print(f"Error loading budgets: {e}")
            return {}

def budget_tracker_menu(current_user):
    """Budget tracker menu showing profile with salary and transaction percentages"""
    utilities = Utilities()
    tracker = BudgetTracker(current_user['id'])
    
    while True:
        print("\n" + "="*60)
        print("           💰 BUDGET TRACKER - PROFILE OVERVIEW")
        print("="*60)
        
        # Get user's transactions
        transactions = tracker._transaction_manager.view_transactions(current_user['id'])
        
        if not transactions:
            print("\n❌ No transactions found. Add some transactions first!")
            utilities.pause()
            return
        
        # Calculate total salary (income)
        total_salary = sum(float(t['amount']) for t in transactions if t['type'] == 'income')
        
        if total_salary == 0:
            print("\n❌ No salary/income found. Add income transactions first!")
            utilities.pause()
            return
        
        print(f"\n📊 SALARY OVERVIEW:")
        print(f"   Total Salary: ${total_salary:.2f}")
        print(f"   Total Transactions: {len(transactions)}")
        
        print(f"\n💸 TRANSACTION BREAKDOWN:")
        print(f"{'Date':<12} {'Type':<8} {'Category':<15} {'Amount':<12} {'% of Salary':<12}")
        print("-" * 70)
        
        # Show each transaction with percentage of salary
        for transaction in sorted(transactions, key=lambda x: x['date'], reverse=True):
            amount = float(transaction['amount'])
            percentage = (amount / total_salary * 100) if total_salary > 0 else 0
            trans_type = "💰" if transaction['type'] == 'income' else "💸"
            
            print(f"{transaction['date']:<12} {trans_type:<8} {transaction['category']:<15} ${amount:<11.2f} {percentage:<11.1f}%")
        
        # Show spending summary
        total_expenses = sum(float(t['amount']) for t in transactions if t['type'] == 'expense')
        total_income = sum(float(t['amount']) for t in transactions if t['type'] == 'income')
        net_worth = total_income - total_expenses
        
        print(f"\n📈 FINANCIAL SUMMARY:")
        print(f"   Total Income: ${total_income:.2f}")
        print(f"   Total Expenses: ${total_expenses:.2f}")
        print(f"   Net Worth: ${net_worth:.2f}")
        print(f"   Expense % of Income: {(total_expenses/total_income*100):.1f}%")
        
        print(f"\nOptions:")
        print("1. Set Monthly Budget")
        print("2. View Budget Status")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n--- Set Monthly Budget ---")
            category = input("Enter category (Food, Transport, Bills, etc.): ").strip()
            try:
                amount = float(input("Enter budget amount: "))
                if tracker.set_monthly_budget(category, amount):
                    print(f"✅ Budget set for {category}: ${amount:.2f}")
                else:
                    print("❌ Failed to set budget")
            except ValueError:
                print("❌ Invalid amount")
            utilities.pause()
            
        elif choice == "2":
            print("\n--- Budget Status ---")
            status = tracker.get_budget_status()
            if "message" in status:
                print(f"ℹ️  {status['message']}")
            else:
                print(f"{'Category':<15} {'Budget':<12} {'Spent':<12} {'Remaining':<12} {'% Used':<10}")
                print("-" * 70)
                for category, data in status.items():
                    print(f"{category:<15} ${data['budget']:<11.2f} ${data['spent']:<11.2f} ${data['remaining']:<11.2f} {data['percentage']:<9.1f}%")
            utilities.pause()
            
        elif choice == "3":
            break
            
        else:
            print("❌ Invalid choice!")
            utilities.pause()

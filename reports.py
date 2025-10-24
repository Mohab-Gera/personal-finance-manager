from typing import Dict, List
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict

# Import the transactions module to get user transactions
import transactions

class ReportsManager:
   
    def __init__(self, user_id: str):
        
        self.user_id = user_id
        self.transactions = self._load_user_transactions()
    
    def _load_user_transactions(self) -> List[Dict]:
        
        try:
            # Use the existing transactions module to get user's transactions
            return transactions.view_transactions(self.user_id)
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
    
    def generate_dashboard(self) -> Dict:
        
        print("\n" + "="*50)
        print
        print("="*50)
        
        # Calculate total income and expenses
        total_income = 0
        total_expenses = 0
        
        # Count transactions
        income_count = 0
        expense_count = 0
        
        # Get current month data
        current_month = datetime.now().strftime('%Y-%m')
        monthly_income = 0
        monthly_expenses = 0
        
        # Loop through all transactions to calculate total
        for transaction in self.transactions:
            amount = float(transaction['amount'])
            
            if transaction['type'] == 'income':
                total_income += amount
                income_count += 1
                # Check sum of income for current month
            
                if transaction['date'].startswith(current_month):
                    monthly_income += amount
            else:  # expense
                total_expenses += amount
                expense_count += 1
                # Check if from current month
                if transaction['date'].startswith(current_month):
                    monthly_expenses += amount
        
        # Calculate net worth (income - expenses)
        net_worth = total_income - total_expenses
        monthly_net = monthly_income - monthly_expenses
        
        # Display the dashboard
        print(f"\n TOTAL INCOME: ${total_income:.2f} ({income_count} transactions)")
       
from typing import Dict, List
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict

# Import the transactions module to get user transactions
from transactions import TransactionManager

class ReportsManager:
    """
    This class handles all the reporting functionality for the Personal Finance Manager.
    It uses Object-Oriented Programming to organize the code better.
    """
    
    def __init__(self, user_id: str):
        """
        Set up reports for a specific user
        """
        self.user_id = user_id
        self.transactions = self._load_user_transactions()
    
    def _load_user_transactions(self) -> List[Dict]:
        """
        Load all transactions for this user
        This is a helper method (starts with _) that other methods use
        """
        try:
            # Use the TransactionManager to get user's transactions
            tm = TransactionManager()
            return tm.view_transactions(self.user_id)
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
    
    def generate_dashboard(self) -> Dict:
        """
        Create a dashboard summary showing overall financial health
        This is like a quick overview of your money situation
        """
        print("\n" + "="*50)
        print("           DASHBOARD SUMMARY")
        print("="*50)
        
        # Calculate totals for income and expenses
        total_income = 0
        total_expenses = 0
        
        # Count transactions
        income_count = 0
        expense_count = 0
        
        # Get current month data
        current_month = datetime.now().strftime('%Y-%m')
        monthly_income = 0
        monthly_expenses = 0
        
        # Loop through all transactions to calculate totals
        for transaction in self.transactions:
            amount = float(transaction['amount'])
            
            if transaction['type'] == 'income':
                total_income += amount
                income_count += 1
                # Check if it's from current month
                if transaction['date'].startswith(current_month):
                    monthly_income += amount
            else:  # expense
                total_expenses += amount
                expense_count += 1
                # Check if it's from current month
                if transaction['date'].startswith(current_month):
                    monthly_expenses += amount
        
        # Calculate net worth (income - expenses)
        net_worth = total_income - total_expenses
        monthly_net = monthly_income - monthly_expenses
        
        # Show dashboard
        print(f"\nTOTAL INCOME: ${total_income:.2f} ({income_count} transactions)")
        print(f"TOTAL EXPENSES: ${total_expenses:.2f} ({expense_count} transactions)")
        print(f"NET WORTH: ${net_worth:.2f}")
        print("-" * 50)
        print(f"THIS MONTH ({current_month}):")
        print(f"   Income: ${monthly_income:.2f}")
        print(f"   Expenses: ${monthly_expenses:.2f}")
        print(f"   Net: ${monthly_net:.2f}")
        
        # Show financial health status
        if net_worth > 0:
            print(f"\nFinancial Status: POSITIVE (${net_worth:.2f} saved)")
        else:
            print(f"\nFinancial Status: NEGATIVE (${abs(net_worth):.2f} in debt)")
        
        # Return data for potential use by other methods
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_worth': net_worth,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'monthly_net': monthly_net
        }
    
    def generate_monthly_report(self, month: int, year: int) -> Dict:
        """
        Create a detailed report for a specific month
        This shows you exactly what happened in that month
        """
        print(f"\n" + "="*50)
        print(f"        MONTHLY REPORT - {month:02d}/{year}")
        print("="*50)
        
        # Filter transactions for the specific month
        month_transactions = []
        for transaction in self.transactions:
            trans_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
            if trans_date.month == month and trans_date.year == year:
                month_transactions.append(transaction)
        
        if not month_transactions:
            print(f"\nNo transactions found for {month:02d}/{year}")
            return {}
        
        # Calculate monthly totals
        monthly_income = 0
        monthly_expenses = 0
        income_by_category = defaultdict(float)
        expense_by_category = defaultdict(float)
        
        # Process each transaction
        for transaction in month_transactions:
            amount = float(transaction['amount'])
            category = transaction['category']
            
            if transaction['type'] == 'income':
                monthly_income += amount
                income_by_category[category] += amount
            else:
                monthly_expenses += amount
                expense_by_category[category] += amount
        
        # Display monthly summary
        monthly_net = monthly_income - monthly_expenses
        print(f"\nMONTHLY INCOME: ${monthly_income:.2f}")
        print(f"MONTHLY EXPENSES: ${monthly_expenses:.2f}")
        print(f"MONTHLY NET: ${monthly_net:.2f}")
        print(f"TOTAL TRANSACTIONS: {len(month_transactions)}")
        
        # Show income breakdown by category
        if income_by_category:
            print(f"\nINCOME BREAKDOWN:")
            for category, amount in income_by_category.items():
                percentage = (amount / monthly_income * 100) if monthly_income > 0 else 0
                print(f"   {category}: ${amount:.2f} ({percentage:.1f}%)")
        
        # Show expense breakdown by category
        if expense_by_category:
            print(f"\n💸 EXPENSE BREAKDOWN:")
            for category, amount in expense_by_category.items():
                percentage = (amount / monthly_expenses * 100) if monthly_expenses > 0 else 0
                print(f"   {category}: ${amount:.2f} ({percentage:.1f}%)")
        
        # Show recent transactions
        print(f"\n📋 RECENT TRANSACTIONS ({month:02d}/{year}):")
        for transaction in sorted(month_transactions, key=lambda x: x['date'], reverse=True)[:10]:
            trans_type = "💰" if transaction['type'] == 'income' else "💸"
            print(f"   {trans_type} {transaction['date']} - {transaction['category']} - ${transaction['amount']}")
            print(f"      {transaction['description']}")
        
        return {
            'month': month,
            'year': year,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'monthly_net': monthly_net,
            'transaction_count': len(month_transactions),
            'income_by_category': dict(income_by_category),
            'expense_by_category': dict(expense_by_category)
        }
    
    def generate_category_breakdown(self) -> Dict:
        """
        Show spending breakdown by category
        This helps you see where your money goes
        """
        print("\n" + "="*50)
        print("        📊 CATEGORY BREAKDOWN")
        print("="*50)
        
        # Group transactions by category
        income_by_category = defaultdict(float)
        expense_by_category = defaultdict(float)
        category_counts = defaultdict(int)
        
        # Process all transactions
        for transaction in self.transactions:
            amount = float(transaction['amount'])
            category = transaction['category']
            category_counts[category] += 1
            
            if transaction['type'] == 'income':
                income_by_category[category] += amount
            else:
                expense_by_category[category] += amount
        
        # Calculate totals
        total_income = sum(income_by_category.values())
        total_expenses = sum(expense_by_category.values())
        
        # Display income categories
        if income_by_category:
            print(f"\n💰 INCOME BY CATEGORY:")
            for category, amount in sorted(income_by_category.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_income * 100) if total_income > 0 else 0
                count = category_counts[category]
                print(f"   {category}: ${amount:.2f} ({percentage:.1f}%) - {count} transactions")
        
        # Display expense categories
        if expense_by_category:
            print(f"\n💸 EXPENSES BY CATEGORY:")
            for category, amount in sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                count = category_counts[category]
                print(f"   {category}: ${amount:.2f} ({percentage:.1f}%) - {count} transactions")
        
        # Show top spending categories
        if expense_by_category:
            print(f"\n🏆 TOP SPENDING CATEGORIES:")
            sorted_expenses = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)
            for i, (category, amount) in enumerate(sorted_expenses[:5], 1):
                print(f"   {i}. {category}: ${amount:.2f}")
        
        return {
            'income_by_category': dict(income_by_category),
            'expense_by_category': dict(expense_by_category),
            'total_income': total_income,
            'total_expenses': total_expenses,
            'category_counts': dict(category_counts)
        }
    
    def generate_spending_trends(self) -> List[Dict]:
        """
        Show spending trends over time
        This helps you see if you're spending more or less over time
        """
        print("\n" + "="*50)
        print("        📈 SPENDING TRENDS")
        print("="*50)
        
        # Group transactions by month
        monthly_data = defaultdict(lambda: {'income': 0, 'expenses': 0, 'count': 0})
        
        # Process all transactions
        for transaction in self.transactions:
            # Extract year-month from date
            date_parts = transaction['date'].split('-')
            year_month = f"{date_parts[0]}-{date_parts[1]}"
            amount = float(transaction['amount'])
            
            monthly_data[year_month][transaction['type']] += amount
            monthly_data[year_month]['count'] += 1
        
        if not monthly_data:
            print("\n❌ No transaction data available for trends")
            return []
        
        # Sort by date
        sorted_months = sorted(monthly_data.items())
        
        print(f"\n📅 MONTHLY TRENDS:")
        print(f"{'Month':<12} {'Income':<12} {'Expenses':<12} {'Net':<12} {'Count':<8}")
        print("-" * 60)
        
        trends_data = []
        for month, data in sorted_months:
            net = data['income'] - data['expenses']
            print(f"{month:<12} ${data['income']:<11.2f} ${data['expenses']:<11.2f} ${net:<11.2f} {data['count']:<8}")
            
            trends_data.append({
                'month': month,
                'income': data['income'],
                'expenses': data['expenses'],
                'net': net,
                'count': data['count']
            })
        
        # Calculate trend analysis
        if len(trends_data) >= 2:
            print(f"\n📊 TREND ANALYSIS:")
            recent = trends_data[-1]
            previous = trends_data[-2]
            
            income_change = recent['income'] - previous['income']
            expense_change = recent['expenses'] - previous['expenses']
            
            print(f"   Last month vs previous:")
            print(f"   Income change: ${income_change:+.2f}")
            print(f"   Expense change: ${expense_change:+.2f}")
            
            if expense_change > 0:
                print(f"   ⚠️  Spending increased by ${expense_change:.2f}")
            elif expense_change < 0:
                print(f"   ✅ Spending decreased by ${abs(expense_change):.2f}")
            else:
                print(f"   ➡️  Spending stayed the same")
        
        return trends_data

# Keep the original menu function but update it to use the new class
def reports_menu(current_user):
    """
    Main reports menu - this is the entry point for all reports
    """
    while True:
        print("\n------ Reports Menu ------")
        print("1. Dashboard Summary")
        print("2. Monthly Report")
        print("3. Category Breakdown")
        print("4. Spending Trends")
        print("5. Back to Main Menu")
        print("--------------------------")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        # Create a ReportsManager instance for this user
        reports_manager = ReportsManager(current_user['id'])
        
        if choice == "1":
            print("\nGenerating Dashboard Summary...")
            reports_manager.generate_dashboard()
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            try:
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year: "))
                if 1 <= month <= 12 and year > 0:
                    print(f"\nGenerating Monthly Report for {month:02d}/{year}...")
                    reports_manager.generate_monthly_report(month, year)
                else:
                    print("Invalid month or year!")
            except ValueError:
                print("Please enter valid numbers!")
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            print("\nGenerating Category Breakdown...")
            reports_manager.generate_category_breakdown()
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            print("\nGenerating Spending Trends...")
            reports_manager.generate_spending_trends()
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            break
            
        else:
            print("Invalid choice! Please enter 1-5.")
            input("\nPress Enter to continue...")
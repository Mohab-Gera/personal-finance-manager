from typing import Dict, List
from datetime import datetime

# reports_menu()
def reports_menu(current_user):
    while True:
        print("\n------ Reports Menu ------")
        print("1. Dashboard Summary")
        print("2. Monthly Report")
        print("3. Category Breakdown")
        print("4. Spending Trends")
        print("5. Back to Main Menu")
        print("--------------------------")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            generate_dashboard(current_user['id'])
        elif choice == "2":
            month = input("Enter month (1-12): ")
            year = input("Enter year: ")
            generate_monthly_report(current_user['id'], month, year)
        elif choice == "3":
            generate_category_breakdown(current_user['id'])
        elif choice == "4":
            generate_spending_trends(current_user['id'])
        elif choice == "5":
            break
        else:
            print("Invalid choice! Please enter 1-5.")



def generate_dashboard(user_id: str) -> Dict:
    """Generate dashboard summary"""
    pass

def generate_monthly_report(user_id: str, month: int, year: int) -> Dict:
    """Generate monthly financial report"""
    pass

def generate_category_breakdown(user_id: str) -> Dict:
    """Generate spending by category report"""
    pass

def generate_spending_trends(user_id: str) -> List[Dict]:
    """Generate spending trends over time"""
    pass

def export_report(report_data: Dict, format: str = 'pdf') -> bool:
    """Export report in specified format"""
    pass

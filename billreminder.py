from datetime import datetime
from jsonhandler import JsonHandler
from utility import Utilities
from typing import Dict, List, Optional, Any

class BillReminderManager:
    """Manager class for handling bill reminder operations"""
    
    def __init__(self):
        self._json_handler = JsonHandler()
        self._utilities = Utilities()
    
    def add_bill_reminder(self, user_id: str, amount: float, bill_type: str, 
                         category: str, description: str, expected_date: str, 
                         reminder_date: str, recurring: bool = False, 
                         recurrence_interval: str = None) -> Optional[Dict[str, Any]]:
        """Add a new bill reminder"""
        try:
            # Create a mock user object for validation
            class MockUser:
                def __init__(self, user_id, currency='USD'):
                    self.id = user_id
                    self.currency = currency
            
            mock_user = MockUser(user_id)
            
            # Create bill reminder object
            bill = BillReminder(
                user=mock_user,
                amount=amount,
                bill_type=bill_type,
                category=category,
                description=description,
                expected_date=expected_date,
                reminder_date=reminder_date,
                recurring=recurring,
                recurrence_interval=recurrence_interval
            )
            
            # Validate inputs
            if not bill.validate_inputs():
                return None
            
            # Save to storage
            bills_data = self._json_handler.load_bills()
            
            if user_id not in bills_data:
                bills_data[user_id] = []
            
            bill_data = {
                "bill_id": self._utilities.generate_uuid(),
                "user_id": user_id,
                "amount": bill.amount,
                "bill_type": bill.bill_type,
                "category": bill.category,
                "description": bill.description,
                "expected_date": bill.expected_date,
                "reminder_date": bill.reminder_date,
                "status": bill.status,
                "recurring": bill.recurring,
                "recurrence_interval": bill.recurrence_interval,
                "paid_date": bill.paid_date,
                "notification_sent": bill.notification_sent,
                "created_at": bill.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            bills_data[user_id].append(bill_data)
            
            if self._json_handler.save_bills(bills_data):
                return bill_data
            else:
                print("Failed to save bill reminder")
                return None
                
        except Exception as e:
            print(f"Error adding bill reminder: {e}")
            return None
    
    def get_bills_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all bills for a user"""
        return BillReminder.get_all_bills_for_user(user_id)
    
    def mark_bill_as_paid(self, user_id: str, bill_id: str) -> bool:
        """Mark a bill as paid"""
        try:
            bills_data = self._json_handler.load_bills()
            
            if user_id not in bills_data:
                return False
            
            for bill in bills_data[user_id]:
                if bill['bill_id'] == bill_id:
                    bill['status'] = 'Paid'
                    bill['paid_date'] = datetime.now().strftime('%Y-%m-%d')
                    bill['notification_sent'] = True
                    
                    return self._json_handler.save_bills(bills_data)
            
            return False
            
        except Exception as e:
            print(f"Error marking bill as paid: {e}")
            return False
    
    def delete_bill(self, user_id: str, bill_id: str) -> bool:
        """Delete a bill reminder"""
        try:
            bills_data = self._json_handler.load_bills()
            
            if user_id not in bills_data:
                return False
            
            for i, bill in enumerate(bills_data[user_id]):
                if bill['bill_id'] == bill_id:
                    del bills_data[user_id][i]
                    return self._json_handler.save_bills(bills_data)
            
            return False
            
        except Exception as e:
            print(f"Error deleting bill: {e}")
            return False
    
    def get_overdue_bills(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all overdue bills for a user"""
        try:
            bills = self.get_bills_for_user(user_id)
            overdue_bills = []
            
            for bill in bills:
                if bill['status'] != 'Paid':
                    current_date = datetime.now().date()
                    expected_date = datetime.strptime(bill['expected_date'], '%Y-%m-%d').date()
                    
                    if current_date > expected_date:
                        overdue_bills.append(bill)
            
            return overdue_bills
            
        except Exception as e:
            print(f"Error getting overdue bills: {e}")
            return []
    
    def get_upcoming_bills(self, user_id: str, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get bills due within the next N days"""
        try:
            bills = self.get_bills_for_user(user_id)
            upcoming_bills = []
            
            for bill in bills:
                if bill['status'] != 'Paid':
                    current_date = datetime.now().date()
                    expected_date = datetime.strptime(bill['expected_date'], '%Y-%m-%d').date()
                    days_left = (expected_date - current_date).days
                    
                    if 0 <= days_left <= days_ahead:
                        upcoming_bills.append(bill)
            
            return upcoming_bills
            
        except Exception as e:
            print(f"Error getting upcoming bills: {e}")
            return []

class BillReminder:
    def __init__(
        self,
        user,
        amount,
        bill_type,
        category,
        description,
        expected_date,
        reminder_date,
        status="Pending",
        recurring=False,
        recurrence_interval=None,
        paid_date=None,
        notification_sent=False,
        created_at=None
    ):
        # Basic attributes
        self.user = user
        self.user_id = user.id
        self.amount = amount
        self.bill_type = bill_type
        self.category = category
        self.description = description
        self.expected_date = expected_date
        self.reminder_date = reminder_date
        self.status = status
        self.recurring = recurring
        self.recurrence_interval = recurrence_interval
        self.paid_date = paid_date
        self.notification_sent = notification_sent
        self.created_at = created_at or datetime.now()

    # ------------------------------
    # Business Logic Methods
    # ------------------------------

    def send_reminder(self):
        """Send reminder to the user if due date is near."""
        try:
            from datetime import datetime, timedelta
            from utility import Utilities
            
            utilities = Utilities()
            current_date = datetime.now().date()
            expected_date = datetime.strptime(self.expected_date, '%Y-%m-%d').date()
            reminder_date = datetime.strptime(self.reminder_date, '%Y-%m-%d').date()
            
            # Check if it's time to send reminder
            if current_date >= reminder_date and not self.notification_sent:
                days_left = (expected_date - current_date).days
                
                if days_left > 0:
                    print(f"\n🔔 BILL REMINDER")
                    print(f"Bill: {self.description}")
                    print(f"Amount: {utilities.format_currency(self.amount, self.user.currency)}")
                    print(f"Due Date: {self.expected_date}")
                    print(f"Days Left: {days_left}")
                    print("-" * 40)
                    
                    self.notification_sent = True
                    return True
                elif days_left == 0:
                    print(f"\n⚠️  BILL DUE TODAY")
                    print(f"Bill: {self.description}")
                    print(f"Amount: {utilities.format_currency(self.amount, self.user.currency)}")
                    print(f"Due Date: {self.expected_date}")
                    print("-" * 40)
                    
                    self.notification_sent = True
                    return True
                else:
                    print(f"\n🚨 OVERDUE BILL")
                    print(f"Bill: {self.description}")
                    print(f"Amount: {utilities.format_currency(self.amount, self.user.currency)}")
                    print(f"Due Date: {self.expected_date}")
                    print(f"Days Overdue: {abs(days_left)}")
                    print("-" * 40)
                    
                    self.notification_sent = True
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error sending reminder: {e}")
            return False

    def mark_as_paid(self):
        """Mark the bill as paid."""
        try:
            from datetime import datetime
            
            if self.status == "Paid":
                print("This bill is already marked as paid.")
                return False
            
            self.status = "Paid"
            self.paid_date = datetime.now().strftime('%Y-%m-%d')
            self.notification_sent = True  # Stop sending reminders
            
            print(f"Bill '{self.description}' marked as paid on {self.paid_date}")
            return True
            
        except Exception as e:
            print(f"Error marking bill as paid: {e}")
            return False

    def stop(self):
        """Stop reminders if the bill is no longer recurring."""
        try:
            if self.recurring:
                self.recurring = False
                self.notification_sent = True  # Stop sending reminders
                print(f"Recurring reminders stopped for bill '{self.description}'")
                return True
            else:
                print("This bill is not set as recurring.")
                return False
                
        except Exception as e:
            print(f"Error stopping reminders: {e}")
            return False

    def is_overdue(self):
        """Check if the bill is overdue."""
        try:
            from datetime import datetime
            
            if self.status == "Paid":
                return False
                
            current_date = datetime.now().date()
            expected_date = datetime.strptime(self.expected_date, '%Y-%m-%d').date()
            
            return current_date > expected_date
            
        except Exception as e:
            print(f"Error checking overdue status: {e}")
            return False

    # ------------------------------
    # Validation Methods
    # ------------------------------

    def validate_amount(self):
        """Ensure the amount is positive."""
        try:
            if not isinstance(self.amount, (int, float)):
                return False
            return self.amount > 0
        except Exception:
            return False

    def validate_dates(self):
        """Ensure reminder_date < expected_date."""
        try:
            from datetime import datetime
            
            reminder_date = datetime.strptime(self.reminder_date, '%Y-%m-%d').date()
            expected_date = datetime.strptime(self.expected_date, '%Y-%m-%d').date()
            
            return reminder_date < expected_date
            
        except Exception:
            return False

    def validate_type_and_category(self):
        """Ensure type and category are valid."""
        try:
            # Valid bill types
            valid_types = ["utility", "rent", "insurance", "subscription", "loan", "credit_card", "other"]
            
            # Valid categories for each type
            valid_categories = {
                "utility": ["electricity", "water", "gas", "internet", "phone", "cable"],
                "rent": ["rent", "mortgage", "property_tax"],
                "insurance": ["health", "auto", "home", "life"],
                "subscription": ["netflix", "spotify", "gym", "software", "magazine"],
                "loan": ["personal", "student", "car", "home"],
                "credit_card": ["visa", "mastercard", "amex", "discover"],
                "other": ["medical", "legal", "maintenance", "other"]
            }
            
            if self.bill_type.lower() not in valid_types:
                return False
                
            if self.category.lower() not in valid_categories.get(self.bill_type.lower(), []):
                return False
                
            return True
            
        except Exception:
            return False

    def validate_inputs(self):
        """Run all validation checks."""
        try:
            errors = []
            
            if not self.validate_amount():
                errors.append("Amount must be a positive number")
                
            if not self.validate_dates():
                errors.append("Reminder date must be before expected date")
                
            if not self.validate_type_and_category():
                errors.append("Invalid bill type or category")
                
            if not self.description or not self.description.strip():
                errors.append("Description cannot be empty")
                
            if self.recurring and not self.recurrence_interval:
                errors.append("Recurrence interval is required for recurring bills")
                
            if errors:
                print("Validation errors:")
                for error in errors:
                    print(f"- {error}")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error during validation: {e}")
            return False

    # ------------------------------
    # CLI Interaction Methods
    # ------------------------------

    def get_user_input(self):
        """Handle user inputs from CLI."""
        try:
            from utility import Utilities
            
            utilities = Utilities()
            
            print("\n=== Add New Bill Reminder ===")
            
            # Get amount
            while True:
                amount_input = input("Amount: ").strip()
                if utilities.validate_amount(amount_input):
                    self.amount = float(amount_input)
                    break
                print("Invalid amount. Please enter a positive number.")
            
            # Get bill type
            print("\nBill Types: utility, rent, insurance, subscription, loan, credit_card, other")
            while True:
                self.bill_type = input("Bill Type: ").strip().lower()
                if self.bill_type in ["utility", "rent", "insurance", "subscription", "loan", "credit_card", "other"]:
                    break
                print("Invalid bill type. Please choose from the list above.")
            
            # Get category based on bill type
            categories = {
                "utility": ["electricity", "water", "gas", "internet", "phone", "cable"],
                "rent": ["rent", "mortgage", "property_tax"],
                "insurance": ["health", "auto", "home", "life"],
                "subscription": ["netflix", "spotify", "gym", "software", "magazine"],
                "loan": ["personal", "student", "car", "home"],
                "credit_card": ["visa", "mastercard", "amex", "discover"],
                "other": ["medical", "legal", "maintenance", "other"]
            }
            
            print(f"\nCategories for {self.bill_type}: {', '.join(categories[self.bill_type])}")
            while True:
                self.category = input("Category: ").strip().lower()
                if self.category in categories[self.bill_type]:
                    break
                print(f"Invalid category. Please choose from: {', '.join(categories[self.bill_type])}")
            
            # Get description
            while True:
                self.description = input("Description: ").strip()
                if self.description:
                    break
                print("Description cannot be empty.")
            
            # Get expected date
            while True:
                expected_date = input("Expected Date (YYYY-MM-DD): ").strip()
                if utilities.validate_date(expected_date):
                    self.expected_date = expected_date
                    break
                print("Invalid date format. Please use YYYY-MM-DD.")
            
            # Get reminder date
            while True:
                reminder_date = input("Reminder Date (YYYY-MM-DD): ").strip()
                if utilities.validate_date(reminder_date):
                    if reminder_date < self.expected_date:
                        self.reminder_date = reminder_date
                        break
                    else:
                        print("Reminder date must be before expected date.")
                else:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            
            # Get recurring status
            recurring_input = input("Is this a recurring bill? (y/n): ").strip().lower()
            self.recurring = recurring_input in ['y', 'yes']
            
            if self.recurring:
                print("Recurrence intervals: daily, weekly, monthly, yearly")
                while True:
                    self.recurrence_interval = input("Recurrence Interval: ").strip().lower()
                    if self.recurrence_interval in ["daily", "weekly", "monthly", "yearly"]:
                        break
                    print("Invalid interval. Please choose from: daily, weekly, monthly, yearly")
            
            return True
            
        except Exception as e:
            print(f"Error getting user input: {e}")
            return False

    def display_bill_info(self):
        """Display bill details in a formatted way."""
        try:
            from utility import Utilities
            
            utilities = Utilities()
            
            print("\n" + "="*50)
            print("           BILL REMINDER DETAILS")
            print("="*50)
            print(f"Description: {self.description}")
            print(f"Amount: {utilities.format_currency(self.amount, self.user.currency)}")
            print(f"Type: {self.bill_type.title()}")
            print(f"Category: {self.category.title()}")
            print(f"Expected Date: {self.expected_date}")
            print(f"Reminder Date: {self.reminder_date}")
            print(f"Status: {self.status}")
            print(f"Recurring: {'Yes' if self.recurring else 'No'}")
            
            if self.recurring and self.recurrence_interval:
                print(f"Recurrence: {self.recurrence_interval.title()}")
            
            if self.paid_date:
                print(f"Paid Date: {self.paid_date}")
            
            if self.is_overdue():
                print("⚠️  STATUS: OVERDUE")
            elif self.status == "Paid":
                print("✅ STATUS: PAID")
            else:
                days_left = self.calculate_days_left(self.expected_date)
                if days_left > 0:
                    print(f"⏰ Days Left: {days_left}")
                else:
                    print("⚠️  Due Today")
            
            print("="*50)
            
        except Exception as e:
            print(f"Error displaying bill info: {e}")

    def show_notifications(self):
        """Show reminders or overdue notifications."""
        try:
            if self.status == "Paid":
                return False
                
            if self.send_reminder():
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error showing notifications: {e}")
            return False

    def edit_bill(self):
        """Allow editing existing bill details."""
        try:
            from utility import Utilities
            
            utilities = Utilities()
            
            print("\n=== Edit Bill Reminder ===")
            print("Current bill details:")
            self.display_bill_info()
            
            while True:
                print("\nWhat would you like to edit?")
                print("1. Amount")
                print("2. Description")
                print("3. Expected Date")
                print("4. Reminder Date")
                print("5. Bill Type")
                print("6. Category")
                print("7. Recurring Status")
                print("8. Save and Exit")
                print("9. Cancel")
                
                choice = input("\nEnter your choice (1-9): ").strip()
                
                if choice == "1":
                    while True:
                        amount_input = input(f"New amount (current: {self.amount}): ").strip()
                        if utilities.validate_amount(amount_input):
                            self.amount = float(amount_input)
                            print("Amount updated!")
                            break
                        print("Invalid amount. Please enter a positive number.")
                
                elif choice == "2":
                    new_desc = input(f"New description (current: {self.description}): ").strip()
                    if new_desc:
                        self.description = new_desc
                        print("Description updated!")
                    else:
                        print("Description cannot be empty.")
                
                elif choice == "3":
                    while True:
                        new_date = input(f"New expected date (current: {self.expected_date}): ").strip()
                        if utilities.validate_date(new_date):
                            self.expected_date = new_date
                            print("Expected date updated!")
                            break
                        print("Invalid date format. Please use YYYY-MM-DD.")
                
                elif choice == "4":
                    while True:
                        new_reminder = input(f"New reminder date (current: {self.reminder_date}): ").strip()
                        if utilities.validate_date(new_reminder):
                            if new_reminder < self.expected_date:
                                self.reminder_date = new_reminder
                                print("Reminder date updated!")
                                break
                            else:
                                print("Reminder date must be before expected date.")
                        else:
                            print("Invalid date format. Please use YYYY-MM-DD.")
                
                elif choice == "5":
                    print("Bill Types: utility, rent, insurance, subscription, loan, credit_card, other")
                    while True:
                        new_type = input(f"New bill type (current: {self.bill_type}): ").strip().lower()
                        if new_type in ["utility", "rent", "insurance", "subscription", "loan", "credit_card", "other"]:
                            self.bill_type = new_type
                            print("Bill type updated!")
                            break
                        print("Invalid bill type. Please choose from the list above.")
                
                elif choice == "6":
                    categories = {
                        "utility": ["electricity", "water", "gas", "internet", "phone", "cable"],
                        "rent": ["rent", "mortgage", "property_tax"],
                        "insurance": ["health", "auto", "home", "life"],
                        "subscription": ["netflix", "spotify", "gym", "software", "magazine"],
                        "loan": ["personal", "student", "car", "home"],
                        "credit_card": ["visa", "mastercard", "amex", "discover"],
                        "other": ["medical", "legal", "maintenance", "other"]
                    }
                    print(f"Categories for {self.bill_type}: {', '.join(categories[self.bill_type])}")
                    while True:
                        new_category = input(f"New category (current: {self.category}): ").strip().lower()
                        if new_category in categories[self.bill_type]:
                            self.category = new_category
                            print("Category updated!")
                            break
                        print(f"Invalid category. Please choose from: {', '.join(categories[self.bill_type])}")
                
                elif choice == "7":
                    recurring_input = input(f"Recurring? (current: {'Yes' if self.recurring else 'No'}) (y/n): ").strip().lower()
                    self.recurring = recurring_input in ['y', 'yes']
                    if self.recurring and not self.recurrence_interval:
                        print("Recurrence intervals: daily, weekly, monthly, yearly")
                        while True:
                            self.recurrence_interval = input("Recurrence Interval: ").strip().lower()
                            if self.recurrence_interval in ["daily", "weekly", "monthly", "yearly"]:
                                break
                            print("Invalid interval. Please choose from: daily, weekly, monthly, yearly")
                    print("Recurring status updated!")
                
                elif choice == "8":
                    if self.validate_inputs():
                        print("Bill updated successfully!")
                        return True
                    else:
                        print("Please fix validation errors before saving.")
                
                elif choice == "9":
                    print("Edit cancelled.")
                    return False
                
                else:
                    print("Invalid choice. Please try again.")
            
        except Exception as e:
            print(f"Error editing bill: {e}")
            return False

    # ------------------------------
    # Class-Level / Utility Methods
    # ------------------------------

    @classmethod
    def get_all_bills_for_user(cls, user_id):
        """Return all bills for a specific user."""
        try:
            from jsonhandler import JsonHandler
            
            json_handler = JsonHandler()
            bills_data = json_handler.load_bills()
            
            if user_id not in bills_data:
                return []
            
            return bills_data[user_id]
            
        except Exception as e:
            print(f"Error getting bills for user: {e}")
            return []

    @staticmethod
    def calculate_days_left(expected_date):
        """Return number of days left until due date."""
        try:
            from datetime import datetime
            
            current_date = datetime.now().date()
            expected_date_obj = datetime.strptime(expected_date, '%Y-%m-%d').date()
            
            return (expected_date_obj - current_date).days
            
        except Exception as e:
            print(f"Error calculating days left: {e}")
            return 0

def bill_reminder_menu(current_user: Dict[str, Any]) -> None:
    """Bill reminder menu interface"""
    manager = BillReminderManager()
    utilities = Utilities()
    
    while True:
        print("\n------ Bill Reminders Menu ------")
        print("1. Add Bill Reminder")
        print("2. View All Bills")
        print("3. View Overdue Bills")
        print("4. View Upcoming Bills")
        print("5. Mark Bill as Paid")
        print("6. Delete Bill Reminder")
        print("7. Show Notifications")
        print("8. Back to Main Menu")
        print("--------------------------------")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            try:
                print("\nAdding new bill reminder...")
                
                # Get amount
                while True:
                    amount_input = input("Amount: ").strip()
                    if utilities.validate_amount(amount_input):
                        amount = float(amount_input)
                        break
                    print("Invalid amount. Please enter a positive number.")
                
                # Get bill type
                print("\nBill Types: utility, rent, insurance, subscription, loan, credit_card, other")
                while True:
                    bill_type = input("Bill Type: ").strip().lower()
                    if bill_type in ["utility", "rent", "insurance", "subscription", "loan", "credit_card", "other"]:
                        break
                    print("Invalid bill type. Please choose from the list above.")
                
                # Get category based on bill type
                categories = {
                    "utility": ["electricity", "water", "gas", "internet", "phone", "cable"],
                    "rent": ["rent", "mortgage", "property_tax"],
                    "insurance": ["health", "auto", "home", "life"],
                    "subscription": ["netflix", "spotify", "gym", "software", "magazine"],
                    "loan": ["personal", "student", "car", "home"],
                    "credit_card": ["visa", "mastercard", "amex", "discover"],
                    "other": ["medical", "legal", "maintenance", "other"]
                }
                
                print(f"\nCategories for {bill_type}: {', '.join(categories[bill_type])}")
                while True:
                    category = input("Category: ").strip().lower()
                    if category in categories[bill_type]:
                        break
                    print(f"Invalid category. Please choose from: {', '.join(categories[bill_type])}")
                
                # Get description
                while True:
                    description = input("Description: ").strip()
                    if description:
                        break
                    print("Description cannot be empty.")
                
                # Get expected date
                while True:
                    expected_date = input("Expected Date (YYYY-MM-DD): ").strip()
                    if utilities.validate_date(expected_date):
                        break
                    print("Invalid date format. Please use YYYY-MM-DD.")
                
                # Get reminder date
                while True:
                    reminder_date = input("Reminder Date (YYYY-MM-DD): ").strip()
                    if utilities.validate_date(reminder_date):
                        if reminder_date < expected_date:
                            break
                        else:
                            print("Reminder date must be before expected date.")
                    else:
                        print("Invalid date format. Please use YYYY-MM-DD.")
                
                # Get recurring status
                recurring_input = input("Is this a recurring bill? (y/n): ").strip().lower()
                recurring = recurring_input in ['y', 'yes']
                recurrence_interval = None
                
                if recurring:
                    print("Recurrence intervals: daily, weekly, monthly, yearly")
                    while True:
                        recurrence_interval = input("Recurrence Interval: ").strip().lower()
                        if recurrence_interval in ["daily", "weekly", "monthly", "yearly"]:
                            break
                        print("Invalid interval. Please choose from: daily, weekly, monthly, yearly")
                
                bill_data = manager.add_bill_reminder(
                    current_user['id'],
                    amount,
                    bill_type,
                    category,
                    description,
                    expected_date,
                    reminder_date,
                    recurring,
                    recurrence_interval
                )
                
                if bill_data:
                    print("\nBill reminder added successfully!")
                else:
                    print("\nFailed to add bill reminder.")
                
            except Exception as e:
                print(f"\nError: {e}")
            utilities.pause()
            
        elif choice == "2":
            print("\nViewing all bills...")
            bills = manager.get_bills_for_user(current_user['id'])
            if bills:
                print(f"\n--- Your Bills ({len(bills)}) ---")
                for idx, bill in enumerate(bills, 1):
                    status_icon = "✅" if bill['status'] == 'Paid' else "⏰"
                    print(f"\n[{idx}] {status_icon} {bill['description']}")
                    print(f"    Amount: {utilities.format_currency(bill['amount'], current_user.get('currency', 'USD'))}")
                    print(f"    Type: {bill['bill_type'].title()} | Category: {bill['category'].title()}")
                    print(f"    Due Date: {bill['expected_date']} | Status: {bill['status']}")
                    if bill['recurring']:
                        print(f"    Recurring: {bill['recurrence_interval'].title()}")
                    print("-" * 50)
            else:
                print("\nNo bills found.")
            utilities.pause()
            
        elif choice == "3":
            print("\nViewing overdue bills...")
            overdue_bills = manager.get_overdue_bills(current_user['id'])
            if overdue_bills:
                print(f"\n--- Overdue Bills ({len(overdue_bills)}) ---")
                for idx, bill in enumerate(overdue_bills, 1):
                    print(f"\n[{idx}] 🚨 {bill['description']}")
                    print(f"    Amount: {utilities.format_currency(bill['amount'], current_user.get('currency', 'USD'))}")
                    print(f"    Due Date: {bill['expected_date']}")
                    print(f"    Type: {bill['bill_type'].title()}")
                    print("-" * 50)
            else:
                print("\nNo overdue bills found.")
            utilities.pause()
            
        elif choice == "4":
            print("\nViewing upcoming bills (next 7 days)...")
            upcoming_bills = manager.get_upcoming_bills(current_user['id'], 7)
            if upcoming_bills:
                print(f"\n--- Upcoming Bills ({len(upcoming_bills)}) ---")
                for idx, bill in enumerate(upcoming_bills, 1):
                    days_left = BillReminder.calculate_days_left(bill['expected_date'])
                    print(f"\n[{idx}] ⏰ {bill['description']}")
                    print(f"    Amount: {utilities.format_currency(bill['amount'], current_user.get('currency', 'USD'))}")
                    print(f"    Due Date: {bill['expected_date']} (in {days_left} days)")
                    print(f"    Type: {bill['bill_type'].title()}")
                    print("-" * 50)
            else:
                print("\nNo upcoming bills found.")
            utilities.pause()
            
        elif choice == "5":
            print("\nMarking bill as paid...")
            bills = manager.get_bills_for_user(current_user['id'])
            if not bills:
                print("No bills found.")
                utilities.pause()
                continue
                
            print("\n--- Your Bills ---")
            for idx, bill in enumerate(bills, 1):
                if bill['status'] != 'Paid':
                    print(f"[{idx}] {bill['description']} - {utilities.format_currency(bill['amount'], current_user.get('currency', 'USD'))}")
            
            try:
                choice_idx = int(input("\nEnter bill number to mark as paid (0 to cancel): "))
                if choice_idx == 0:
                    continue
                if 1 <= choice_idx <= len(bills):
                    selected_bill = bills[choice_idx - 1]
                    if manager.mark_bill_as_paid(current_user['id'], selected_bill['bill_id']):
                        print(f"\nBill '{selected_bill['description']}' marked as paid!")
                    else:
                        print("\nFailed to mark bill as paid.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            utilities.pause()
            
        elif choice == "6":
            print("\nDeleting bill reminder...")
            bills = manager.get_bills_for_user(current_user['id'])
            if not bills:
                print("No bills found.")
                utilities.pause()
                continue
                
            print("\n--- Your Bills ---")
            for idx, bill in enumerate(bills, 1):
                status_icon = "✅" if bill['status'] == 'Paid' else "⏰"
                print(f"[{idx}] {status_icon} {bill['description']} - {utilities.format_currency(bill['amount'], current_user.get('currency', 'USD'))}")
            
            try:
                choice_idx = int(input("\nEnter bill number to delete (0 to cancel): "))
                if choice_idx == 0:
                    continue
                if 1 <= choice_idx <= len(bills):
                    selected_bill = bills[choice_idx - 1]
                    confirm = input(f"Are you sure you want to delete '{selected_bill['description']}'? (y/n): ").lower()
                    if confirm == 'y':
                        if manager.delete_bill(current_user['id'], selected_bill['bill_id']):
                            print(f"\nBill '{selected_bill['description']}' deleted successfully!")
                        else:
                            print("\nFailed to delete bill.")
                    else:
                        print("Deletion cancelled.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            utilities.pause()
            
        elif choice == "7":
            print("\nChecking for notifications...")
            bills = manager.get_bills_for_user(current_user['id'])
            notifications_shown = 0
            
            for bill in bills:
                if bill['status'] != 'Paid':
                    # Create a temporary BillReminder object to check notifications
                    class MockUser:
                        def __init__(self, user_id, currency):
                            self.id = user_id
                            self.currency = currency
                    
                    mock_user = MockUser(current_user['id'], current_user.get('currency', 'USD'))
                    
                    temp_bill = BillReminder(
                        user=mock_user,
                        amount=bill['amount'],
                        bill_type=bill['bill_type'],
                        category=bill['category'],
                        description=bill['description'],
                        expected_date=bill['expected_date'],
                        reminder_date=bill['reminder_date'],
                        status=bill['status'],
                        recurring=bill['recurring'],
                        recurrence_interval=bill['recurrence_interval'],
                        paid_date=bill.get('paid_date'),
                        notification_sent=bill.get('notification_sent', False)
                    )
                    
                    if temp_bill.show_notifications():
                        notifications_shown += 1
            
            if notifications_shown == 0:
                print("\nNo notifications at this time.")
            
            utilities.pause()
            
        elif choice == "8":
            print("\nReturning to Main Menu...")
            break
            
        else:
            print("\nInvalid choice! Please enter a number between 1 and 8.")
            utilities.pause()

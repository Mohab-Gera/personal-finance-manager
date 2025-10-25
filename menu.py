from transactions import transactions_menu
import reports
import search_filter
from users import User
from utility import Utilities
from billreminder import bill_reminder_menu
from budget_tracker import budget_tracker_menu

def main_menu(current_user):
    utilities = Utilities()
    
    while True:
        try:
            print("\n========== MAIN MENU ==========")
            print("1. Transactions")
            print("2. Bill Reminders")
            print("3. Budget Tracker")
            print("4. Reports")
            print("5. Search & Filter")
            print("6. User Profile")
            print("7. User Settings")
            print("8. Logout")
            print("================================")

            choice = input("Enter your choice (1-8): ").strip()

            if not choice.isdigit():
                raise ValueError("Input must be a number!")

            choice = int(choice)

            if choice not in range(1, 9):
                raise ValueError("Please enter a number between 1 and 8.")

            if choice == 1:
                print("Opening Transactions Menu...")
                transactions_menu(current_user)

            elif choice == 2:
                print("Opening Bill Reminders Menu...")
                bill_reminder_menu(current_user)

            elif choice == 3:
                print("Opening Budget Tracker...")
                budget_tracker_menu(current_user)

            elif choice == 4:
                print("Opening Reports Menu...")
                reports.reports_menu(current_user)

            elif choice == 5:
                print("Opening Search & Filter Menu...")
                search_filter.search_menu(current_user)

            elif choice == 6:
                print("Displaying User Profile...")
                User.show_user_profile(current_user['id'])
                utilities.pause()

            elif choice == 7:
                while True:
                    print("\n=== User Settings ===")
                    print("1. Switch User")
                    print("2. Change Password")
                    print("3. Delete Account")
                    print("4. Back to Main Menu")
                    print("-------------------")
                    
                    settings_choice = input("Enter your choice (1-4): ").strip()
                    if settings_choice == "1":
                        # Switch User
                        try:
                            new_user = User.login(current_user)
                            if new_user:
                                current_user = new_user
                                print(f"\nSuccessfully switched to user: {current_user['name']}")
                                utilities.pause()
                                break  # Break from settings menu to return to main menu
                        except Exception as e:
                            print(f"\nError switching user: {e}")
                            utilities.pause()                            
                    elif settings_choice == "2":
                        # Change Password
                        try:
                            # Get user object to change password
                            user_obj = User(current_user['name'], "dummy", current_user.get('currency', 'USD'))
                            if user_obj.change_password():
                                print("\nPassword changed successfully!")
                            utilities.pause()
                        except Exception as e:
                            print(f"\nError changing password: {e}")
                            utilities.pause()
                            
                    elif settings_choice == "3":
                        # Delete Account
                        try:
                            confirm = input("Are you sure you want to delete your account? (y/n): ").lower()
                            if confirm == 'y':
                                # Get user object to delete account
                                user_obj = User(current_user['name'], "dummy", current_user.get('currency', 'USD'))
                                if user_obj.delete_user():
                                    print("\nAccount deleted successfully!")
                                    utilities.pause()
                                    return False  # Return to login menu
                            else:
                                print("\nAccount deletion cancelled.")
                                utilities.pause()
                        except Exception as e:
                            print(f"\nError deleting account: {e}")
                            utilities.pause()
                            
                    elif settings_choice == "4":
                        break  # Return to main menu
                        
                    else:
                        print("\nInvalid choice! Please try again.")
                        utilities.pause()

            elif choice == 8:
                print("\nLogging out...")
                utilities.pause()
                return False  # Return to login menu

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        finally:
            print("\n--------------------------------")


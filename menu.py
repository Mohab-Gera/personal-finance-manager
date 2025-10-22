import transactions
import reports
import search_filter
import users
import utilities

def main_menu(current_user):
    while True:
        try:
            print("\n========== MAIN MENU ==========")
            print("1. Transactions")
            print("2. Reports")
            print("3. Search & Filter")
            print("4. User Settings")
            print("5. Logout")
            print("================================")

            choice = input("Enter your choice (1-5): ").strip()

            if not choice.isdigit():
                raise ValueError("Input must be a number!")

            choice = int(choice)

            if choice not in range(1, 6):
                raise ValueError("Please enter a number between 1 and 5.")

            if choice == 1:
                print("Opening Transactions Menu...")
                transactions.transactions_menu(current_user)

            elif choice == 2:
                print("Opening Reports Menu...")
                reports.reports_menu(current_user)

            elif choice == 3:
                print("Opening Search & Filter Menu...")
                search_filter.search_menu(current_user)

            elif choice == 4:
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
                        name = input("Enter username: ").strip()
                        if not name:
                            print("Username cannot be empty!")
                            utilities.pause()
                            continue
                            
                        password = input("Enter password: ").strip()
                        if not password:
                            print("Password cannot be empty!")
                            utilities.pause()
                            continue
                        
                        try:
                            new_user = users.switch_user(name, password, current_user)
                            if new_user:
                                current_user = new_user
                                print(f"\nSuccessfully switched to user: {current_user['name']}")
                                utilities.pause()
                                break  # Break from settings menu to return to main menu
                            else:
                                print("\nInvalid username or password!")
                                utilities.pause()
                        except Exception as e:
                            print(f"\nError switching user: {e}")
                            utilities.pause()                            
                    elif settings_choice == "2":
                        # Change Password
                        try:
                            old_password = input("Enter current password: ").strip()
                            new_password = input("Enter new password: ").strip()
                            if users.change_password(current_user, old_password, new_password):
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
                                if users.delete_user(current_user):
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

            elif choice == 5:
                print("\nLogging out...")
                utilities.pause()
                return False  # Return to login menu

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        finally:
            print("\n--------------------------------")


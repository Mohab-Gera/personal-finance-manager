import os
import sys
from users import User
from menu import main_menu
from utility import Utilities

def init_app():
    """Initialize application and handle user authentication"""
    utilities = Utilities()
    
    while True:
        try:
            utilities.clear_screen()
            print("\n=== Personal Finance Manager ===")
            print("1. Login")
            print("2. Create New Account")
            print("3. Exit")
            print("===============================")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n=== Login ===")
                try:
                    user = User.login()
                    print(f"\nWelcome back, {user['name']}!")
                    utilities.pause()
                    return user
                except ValueError as e:
                    print(f"\nError: {e}")
                    utilities.pause()
                    
            elif choice == "2":
                try:
                    print("\n=== Create New Account ===")
                    name = input("Choose username: ").strip()
                    if not name:
                        raise ValueError("Username cannot be empty")
                        
                    password = input("Choose password: ").strip()
                    if not password:
                        raise ValueError("Password cannot be empty")
                        
                    currency = input("Preferred currency (USD/EUR/GBP): ").strip().upper()
                    if currency not in ["USD", "EUR", "GBP"]:
                        raise ValueError("Invalid currency")
                    
                    user_obj = User(name, password, currency)
                    user = user_obj.get_user_info()
                    print(f"\nAccount created successfully! Welcome {user['name']}!")
                    utilities.pause()
                    return user
                    
                except ValueError as e:
                    print(f"\nError: {e}")
                    utilities.pause()
                    
            elif choice == "3":
                print("\nGoodbye!")
                sys.exit(0)
                
            else:
                print("\nInvalid choice! Please try again.")
                utilities.pause()
                
        except Exception as e:
            print(f"\nCritical error: {e}")
            utilities.pause()

def main():
    try:
        while True:
            # Initialize the app and get authenticated user
            current_user = init_app()
            
            # Launch main menu with authenticated user
            if current_user:
                # If main_menu returns False, it means user logged out
                if not main_menu(current_user):
                    utilities = Utilities()
                    utilities.clear_screen()
                    continue  # Return to login menu
                else:
                    break  # Exit program completely
                    
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
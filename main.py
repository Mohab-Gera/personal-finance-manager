import os
import sys
import users
import menu
import utilities
from utilities import clear_screen, pause

def init_app():
    """Initialize application and handle user authentication"""
    while True:
        try:
            clear_screen()
            print("\n=== Personal Finance Manager ===")
            print("1. Login")
            print("2. Create New Account")
            print("3. Exit")
            print("===============================")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n=== Login ===")
                name = input("Username: ").strip()
                if not name:
                    print("\nUsername cannot be empty!")
                    pause()
                    continue
                    
                password = input("Password: ").strip()
                if not password:
                    print("\nPassword cannot be empty!")
                    pause()
                    continue
                
                user = users.authenticate_user(name, password)
                if user:
                    print(f"\nWelcome back, {user['name']}!")
                    pause()
                    return user
                else:
                    print("\nInvalid username or password!")
                    pause()
                    
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
                    
                    user = users.create_user(name, password, currency)
                    print(f"\nAccount created successfully! Welcome {user['name']}!")
                    pause()
                    return user
                    
                except ValueError as e:
                    print(f"\nError: {e}")
                    pause()
                    
            elif choice == "3":
                print("\nGoodbye!")
                sys.exit(0)
                
            else:
                print("\nInvalid choice! Please try again.")
                pause()
                
        except Exception as e:
            print(f"\nCritical error: {e}")
            pause()

def main():
    try:
        while True:
            # Initialize the app and get authenticated user
            current_user = init_app()
            
            # Launch main menu with authenticated user
            if current_user:
                # If main_menu returns False, it means user logged out
                if not menu.main_menu(current_user):
                    clear_screen()
                    continue  # Return to login menu
                else:
                    break  # Exit program completely
                    
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
import datetime
import hashlib
import os
import uuid

def clear_screen() -> None:
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def hash_password(password: str) -> str:
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

from datetime import datetime

def validate_date(date_string: str) -> bool:
    """Validate if the date string is in correct format YYYY-MM-DD"""
    try:
        if not date_string:
            return False
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
def validate_amount(amount: str) -> bool:
    """Validate if the amount is a valid number"""
    try:
        float_amount = float(amount)
        return float_amount > 0
    except ValueError:
        return False

def generate_transaction_id() -> str:
    """Generate a unique transaction ID"""
    return str(uuid.uuid4())

def pause() -> None:
    """Pause the program execution until user input"""
    input("\nPress Enter to continue...")
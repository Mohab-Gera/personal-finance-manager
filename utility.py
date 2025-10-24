import datetime
import hashlib
import os
import uuid
from typing import Optional
from datetime import datetime


class Utilities:
    """Utility class containing all helper methods for the application"""
    
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate a unique UUID4 string"""
        return str(uuid.uuid4())

    @staticmethod
    def validate_date(date_string: str) -> bool:
        """Validate if the date string is in correct format YYYY-MM-DD"""
        try:
            if not date_string:
                return False
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_amount(amount: str) -> bool:
        """Validate if the amount is a valid number"""
        try:
            float_amount = float(amount)
            return float_amount > 0
        except ValueError:
            return False

    @staticmethod
    def pause() -> None:
        """Pause the program execution until user input"""
        input("\nPress Enter to continue...")

    @staticmethod
    def format_currency(amount: float, currency: str = 'USD') -> str:
        """Format amount as currency string"""
        return f"{currency} {amount:.2f}"

    @staticmethod
    def get_current_date() -> str:
        """Get current date in YYYY-MM-DD format"""
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def is_future_date(date_string: str) -> bool:
        """Check if the given date is in the future"""
        try:
            date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
            return date_obj > datetime.today().date()
        except ValueError:
            return False
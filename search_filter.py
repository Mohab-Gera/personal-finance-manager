from typing import List, Dict
from datetime import datetime

def search_menu(current_user: Dict) -> None:
    """Display search and filter menu"""
    pass

def search_by_date_range(user_id: str, start_date: str, end_date: str) -> List[Dict]:
    """Search transactions by date range"""
    pass

def filter_by_category(user_id: str, category: str) -> List[Dict]:
    """Filter transactions by category"""
    pass

def filter_by_amount_range(user_id: str, min_amount: float, max_amount: float) -> List[Dict]:
    """Filter transactions by amount range"""
    pass

def sort_transactions(user_id: str, key: str = 'amount', reverse: bool = False) -> List[Dict]:
    """Sort transactions by specified key"""
    pass
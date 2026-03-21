"""
Helpers - Common helper functions
"""

from datetime import datetime
from typing import Optional
import hashlib

def format_date(date_str: str, format_type: str = 'display') -> str:
    """
    Format date string for display
    
    Args:
        date_str: Date in YYYY-MM-DD format
        format_type: 'display' or 'relative'
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        if format_type == 'display':
            return date_obj.strftime('%d %b %Y')
        elif format_type == 'relative':
            return get_relative_date(date_obj)
        else:
            return date_str
    except:
        return date_str

def get_relative_date(date_obj: datetime) -> str:
    """Get relative date string (e.g., '2 days ago')"""
    now = datetime.now()
    diff = now - date_obj
    
    days = diff.days
    
    if days == 0:
        return "Today"
    elif days == 1:
        return "Yesterday"
    elif days < 7:
        return f"{days} days ago"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    else:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"

def get_date_difference(date_str: str) -> int:
    """
    Get number of days between date and today
    
    Args:
        date_str: Date in YYYY-MM-DD format
    
    Returns:
        Number of days
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        now = datetime.now()
        diff = now - date_obj
        return diff.days
    except:
        return 0

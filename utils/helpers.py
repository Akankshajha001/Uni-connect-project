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

def truncate_text(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def generate_id(prefix: str = '') -> str:
    """
    Generate a unique ID based on timestamp
    
    Args:
        prefix: Optional prefix for the ID
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{prefix}{timestamp}"

def get_color_for_status(status: str) -> str:
    """
    Get color code for status
    
    Args:
        status: Status string ('open', 'claimed', 'matched')
    
    Returns:
        Color code
    """
    color_map = {
        'open': '#FFA500',      # Orange
        'claimed': '#28A745',    # Green
        'matched': '#007BFF',    # Blue
        'lost': '#DC3545',       # Red
        'found': '#17A2B8'       # Cyan
    }
    return color_map.get(status.lower(), '#6C757D')  # Default Gray

def format_number(num: int, suffix: str = '') -> str:
    """
    Format large numbers with K, M suffixes
    
    Args:
        num: Number to format
        suffix: Optional suffix (e.g., 'downloads')
    """
    if num >= 1000000:
        return f"{num / 1000000:.1f}M {suffix}".strip()
    elif num >= 1000:
        return f"{num / 1000:.1f}K {suffix}".strip()
    else:
        return f"{num} {suffix}".strip()

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename

def calculate_match_percentage(item1: dict, item2: dict) -> float:
    """
    Calculate match percentage between two items
    
    Args:
        item1: First item dictionary
        item2: Second item dictionary
    
    Returns:
        Match percentage (0-100)
    """
    score = 0
    max_score = 3
    
    # Category match
    if item1.get('category', '').lower() == item2.get('category', '').lower():
        score += 1
    
    # Location match
    if item1.get('location', '').lower() == item2.get('location', '').lower():
        score += 1
    
    # Name similarity (simple check)
    name1 = item1.get('item_name', '').lower()
    name2 = item2.get('item_name', '').lower()
    if name1 in name2 or name2 in name1:
        score += 1
    
    return (score / max_score) * 100
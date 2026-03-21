"""
Validators - Input validation functions
"""

import re
from typing import Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format
    Returns: (is_valid, error_message)
    """
    if not email:
        return False, "Email cannot be empty"
    
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    else:
        return False, "Invalid email format"

def validate_roll_no(roll_no: str) -> Tuple[bool, str]:
    """
    Validate roll number format
    Returns: (is_valid, error_message)
    """
    if not roll_no:
        return False, "Roll number cannot be empty"
    
    if len(roll_no) < 3:
        return False, "Roll number too short"
    
    # Allow alphanumeric roll numbers
    if not roll_no.replace('-', '').replace('/', '').isalnum():
        return False, "Roll number should contain only letters, numbers, hyphens, or slashes"
    
    return True, ""

def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate name (should not be empty and reasonable length)
    Returns: (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    if len(name.strip()) < 2:
        return False, "Name too short"
    
    if len(name) > 100:
        return False, "Name too long"
    
    return True, ""

def validate_file_name(file_name: str) -> Tuple[bool, str]:
    """
    Validate file name format
    Returns: (is_valid, error_message)
    """
    if not file_name:
        return False, "File name cannot be empty"
    
    # Check for invalid characters
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in file_name:
            return False, f"File name contains invalid character: {char}"
    
    # Check extension
    if '.' not in file_name:
        return False, "File name should have an extension"
    
    return True, ""

def validate_description(description: str, min_length: int = 10, max_length: int = 500) -> Tuple[bool, str]:
    """
    Validate description text
    Returns: (is_valid, error_message)
    """
    if not description or not description.strip():
        return False, "Description cannot be empty"
    
    desc_length = len(description.strip())
    
    if desc_length < min_length:
        return False, f"Description too short (minimum {min_length} characters)"
    
    if desc_length > max_length:
        return False, f"Description too long (maximum {max_length} characters)"
    
    return True, ""

def validate_category(category: str, valid_categories: list) -> Tuple[bool, str]:
    """
    Validate category against a list of valid categories
    Returns: (is_valid, error_message)
    """
    if not category:
        return False, "Category cannot be empty"
    
    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"
    
    return True, ""
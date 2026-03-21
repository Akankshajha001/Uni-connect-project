"""
Lost & Found Service - Business logic for lost and found items
"""

from datetime import datetime
from typing import List, Dict, Optional
import random
from database.lost_found_db import add_item, get_all_items as db_get_all_items, get_item_by_id as db_get_item_by_id, update_item_status

def generate_verification_code() -> str:
    """Generate a unique 5-digit verification code"""
    return str(random.randint(10000, 99999))

def add_lost_item(item_name: str, category: str, location: str, 
                  description: str, reporter_name: str, reporter_contact: str,
                  image_path: str = None) -> Dict:
    """Add a new lost item to the database (SQLite)"""
    new_item = {
        'type': 'lost',
        'item_name': item_name,
        'category': category,
        'location': location,
        'description': description,
        'reporter_name': reporter_name,
        'reporter_contact': reporter_contact,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'open',
        'matched_with': None,
        'verification_code': generate_verification_code(),
        'image_path': image_path
    }
    new_id = add_item(new_item)
    new_item['id'] = new_id
    return new_item

def add_found_item(item_name: str, category: str, location: str,
                   description: str, reporter_name: str, reporter_contact: str,
                   image_path: str = None) -> Dict:
    """Add a new found item to the database (SQLite)"""
    new_item = {
        'type': 'found',
        'item_name': item_name,
        'category': category,
        'location': location,
        'description': description,
        'reporter_name': reporter_name,
        'reporter_contact': reporter_contact,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'open',
        'matched_with': None,
        'verification_code': generate_verification_code(),
        'image_path': image_path
    }
    new_id = add_item(new_item)
    new_item['id'] = new_id
    return new_item

def get_all_items() -> List[Dict]:
    """Get all lost and found items from SQLite DB"""
    return db_get_all_items()

def get_lost_items() -> List[Dict]:
    """Get only lost items from SQLite DB"""
    return [item for item in db_get_all_items() if item['type'] == 'lost']

def get_found_items() -> List[Dict]:
    """Get only found items from SQLite DB"""
    return [item for item in db_get_all_items() if item['type'] == 'found']

def get_item_by_id(item_id: int) -> Optional[Dict]:
    """Get item by ID from SQLite DB"""
    return db_get_item_by_id(item_id)

def find_potential_matches(item_type: str, category: str, location: str) -> List[Dict]:
    """
    Find potential matches for a lost or found item (SQLite DB)
    Match based on category and location
    """
    opposite_type = 'found' if item_type == 'lost' else 'lost'
    matches = []
    for item in db_get_all_items():
        if item['type'] == opposite_type and item['status'] == 'open':
            if item['category'].lower() == category.lower():
                item_copy = item.copy()
                item_copy['match_score'] = 10
                if item['location'].lower() == location.lower():
                    item_copy['match_score'] = 20
                matches.append(item_copy)
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches

def claim_item(item_id: int, claimer_name: str, verification_detail: str = "", 
               claimer_email: str = "", claimer_contact: str = "") -> bool:
    """
    Mark an item as claimed with verification details (SQLite DB)
    """
    item = db_get_item_by_id(item_id)
    if not item:
        return False
    # Update status in DB
    update_item_status(item_id, 'claimed')
    # Optionally, you can extend update_item_status to store claimer details if needed
    return True

def get_recent_items(limit: int = 10) -> List[Dict]:
    """Get most recent items from SQLite DB"""
    items = db_get_all_items()
    sorted_items = sorted(items, key=lambda x: x['date'], reverse=True)
    return sorted_items[:limit]

def search_items(query: str) -> List[Dict]:
    """Search items by name, category, or location from SQLite DB"""
    query_lower = query.lower()
    results = []
    for item in db_get_all_items():
        if (query_lower in item['item_name'].lower() or 
            query_lower in item['category'].lower() or 
            query_lower in item['location'].lower() or
            query_lower in item['description'].lower()):
            results.append(item)
    return results

def get_items_by_status(status: str) -> List[Dict]:
    """Get items filtered by status from SQLite DB"""
    return [item for item in db_get_all_items() if item['status'] == status]
"""
Analytics Service - Statistics and charts logic
"""


from typing import Dict, List
from database.lost_found_db import get_all_items
from database.notes_db import get_all_notes

def get_lost_found_stats() -> Dict:
    """Get statistics for lost & found items from SQLite DB"""
    items = get_all_items()
    total_items = len(items)
    lost_count = len([item for item in items if item['type'] == 'lost'])
    found_count = len([item for item in items if item['type'] == 'found'])
    open_count = len([item for item in items if item['status'] == 'open'])
    claimed_count = len([item for item in items if item['status'] == 'claimed'])
    return {
        'total_items': total_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'open_count': open_count,
        'claimed_count': claimed_count,
        'match_rate': round((claimed_count / total_items * 100) if total_items > 0 else 0, 2)
    }

def get_notes_stats() -> Dict:
    """Get statistics for notes exchange from SQLite DB"""
    all_notes = get_all_notes()
    total_notes = len(all_notes)
    total_downloads = sum(note['downloads'] for note in all_notes)
    subjects = set(note['subject'] for note in all_notes)
    total_subjects = len(subjects)
    avg_downloads = round(total_downloads / total_notes, 2) if total_notes > 0 else 0
    return {
        'total_notes': total_notes,
        'total_subjects': total_subjects,
        'total_downloads': total_downloads,
        'avg_downloads': avg_downloads,
        'contributors': len(set(note['uploaded_by'] for note in all_notes))
    }

def get_category_distribution() -> Dict[str, int]:
    """Get distribution of items by category from SQLite DB"""
    items = get_all_items()
    categories = {}
    for item in items:
        category = item['category']
        categories[category] = categories.get(category, 0) + 1
    sorted_categories = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    return sorted_categories

def get_location_distribution() -> Dict[str, int]:
    """Get distribution of items by location from SQLite DB"""
    items = get_all_items()
    locations = {}
    for item in items:
        location = item['location']
        locations[location] = locations.get(location, 0) + 1
    return dict(sorted(locations.items(), key=lambda x: x[1], reverse=True))
    
    # Sort by count
    sorted_locations = dict(sorted(locations.items(), key=lambda x: x[1], reverse=True))
    return sorted_locations

def get_top_downloaded_notes(limit: int = 10) -> List[Dict]:
    """Get top downloaded notes from SQLite DB"""
    all_notes = get_all_notes()
    sorted_notes = sorted(all_notes, key=lambda x: x['downloads'], reverse=True)
    return sorted_notes[:limit]

def get_subject_wise_stats() -> Dict[str, Dict]:
    """Get statistics for each subject from SQLite DB"""
    all_notes = get_all_notes()
    subject_stats = {}
    for note in all_notes:
        subject = note['subject']
        if subject not in subject_stats:
            subject_stats[subject] = {'total_notes': 0, 'total_downloads': 0}
        subject_stats[subject]['total_notes'] += 1
        subject_stats[subject]['total_downloads'] += note['downloads']
    for subject in subject_stats:
        total_notes = subject_stats[subject]['total_notes']
        total_downloads = subject_stats[subject]['total_downloads']
        subject_stats[subject]['avg_downloads'] = round(total_downloads / total_notes, 2) if total_notes > 0 else 0
    return subject_stats

def get_user_activity_stats() -> List[Dict]:
    """Get user activity statistics from SQLite DB with actual note counts"""
    from database.users_db import get_all_users
    from database.notes_db import get_notes_count_by_user
    from database.lost_found_db import get_all_items
    
    users = get_all_users()
    all_items = get_all_items()
    activity_list = []
    
    for user_id, user_data in users.items():
        # Count actual notes uploaded by this user (by name)
        actual_notes_count = get_notes_count_by_user(user_data['name'])
        
        # Count actual items reported by this user
        actual_items_count = len([item for item in all_items if item['reporter_name'] == user_data['name']])
        
        activity_list.append({
            'name': user_data['name'],
            'roll_no': user_data['roll_no'],
            'items_reported': actual_items_count,
            'notes_uploaded': actual_notes_count,
            'notes_downloaded': user_data['notes_downloaded'],
            'total_activity': (
                actual_items_count +
                actual_notes_count +
                user_data['notes_downloaded']
            )
        })
    activity_list.sort(key=lambda x: x['total_activity'], reverse=True)
    return activity_list

def get_daily_activity() -> Dict[str, int]:
    """Get item reports by date from SQLite DB"""
    from database.lost_found_db import get_all_items
    items = get_all_items()
    daily_counts = {}
    for item in items:
        date = item['date']
        daily_counts[date] = daily_counts.get(date, 0) + 1
    sorted_daily = dict(sorted(daily_counts.items()))
    return sorted_daily

def get_semester_wise_notes() -> Dict[str, int]:
    """Get notes distribution by semester from SQLite DB"""
    all_notes = get_all_notes()
    semester_counts = {}
    for note in all_notes:
        semester = note['semester']
        semester_counts[semester] = semester_counts.get(semester, 0) + 1
    return semester_counts
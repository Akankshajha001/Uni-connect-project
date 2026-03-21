"""
Notes Exchange Service - Business logic for notes sharing
"""

from datetime import datetime
from typing import List, Dict, Optional
from database import notes_db

def upload_note(subject: str, topic: str, semester: str, uploaded_by: str,
                file_name: str, description: str) -> Dict:
    """Upload a new note to the database (SQLite)"""
    note = {
        'subject': subject,
        'topic': topic,
        'semester': semester,
        'uploaded_by': uploaded_by,
        'file_name': file_name,
        'description': description
    }
    note_id = notes_db.add_note(note)
    note['id'] = note_id
    note['upload_date'] = datetime.now().strftime('%Y-%m-%d')
    note['downloads'] = 0
    note['rating'] = 0.0
    return note

def get_notes_by_subject(subject: str) -> List[Dict]:
    """Get all notes for a specific subject from SQLite DB"""
    return notes_db.get_notes_by_subject(subject)

def get_all_notes_list() -> List[Dict]:
    """Get all notes as a flat list from SQLite DB"""
    return notes_db.get_all_notes()

def get_subjects() -> List[str]:
    """Get list of all available subjects from SQLite DB"""
    all_notes = notes_db.get_all_notes()
    return list(set(note['subject'] for note in all_notes))

def get_note_by_id(note_id: int) -> Optional[Dict]:
    """Get a specific note by ID from SQLite DB"""
    return notes_db.get_note_by_id(note_id)

def increment_download_count(note_id: int) -> bool:
    """Increment the download count for a note in SQLite DB"""
    notes_db.increment_download(note_id)
    return True

def get_top_contributors(limit: int = 10) -> List[Dict]:
    """Get top note contributors based on upload count from SQLite DB"""
    all_notes = notes_db.get_all_notes()
    contributors = {}
    for note in all_notes:
        uploader = note['uploaded_by']
        if uploader not in contributors:
            contributors[uploader] = {
                'name': uploader,
                'uploads': 0,
                'total_downloads': 0,
                'subjects': set()
            }
        contributors[uploader]['uploads'] += 1
        contributors[uploader]['total_downloads'] += note['downloads']
        contributors[uploader]['subjects'].add(note['subject'])
    contributor_list = []
    for contrib in contributors.values():
        contrib['subjects'] = list(contrib['subjects'])
        contributor_list.append(contrib)
    contributor_list.sort(key=lambda x: x['uploads'], reverse=True)
    return contributor_list[:limit]

def search_notes(query: str) -> List[Dict]:
    """Search notes by subject, topic, or description from SQLite DB"""
    query_lower = query.lower()
    results = []
    for note in notes_db.get_all_notes():
        if (query_lower in note['subject'].lower() or
            query_lower in note['topic'].lower() or
            query_lower in note['description'].lower() or
            query_lower in note['uploaded_by'].lower()):
            results.append(note)
    return results

def get_notes_by_semester(semester: str) -> List[Dict]:
    """Get all notes for a specific semester from SQLite DB"""
    results = []
    for note in notes_db.get_all_notes():
        if note['semester'] == semester:
            results.append(note)
    return results

def get_recent_notes(limit: int = 10) -> List[Dict]:
    """Get most recently uploaded notes"""
    all_notes = notes_db.get_all_notes()
    sorted_notes = sorted(all_notes, key=lambda x: x['upload_date'], reverse=True)
    return sorted_notes[:limit]

def get_popular_notes(limit: int = 10) -> List[Dict]:
    """Get most downloaded notes"""
    all_notes = notes_db.get_all_notes()
    sorted_notes = sorted(all_notes, key=lambda x: x['downloads'], reverse=True)
    return sorted_notes[:limit]
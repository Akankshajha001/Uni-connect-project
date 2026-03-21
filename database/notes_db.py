"""
Notes Exchange Database - SQLite persistent storage
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'notes.db')

def _get_conn():
    return sqlite3.connect(DB_PATH)

def _init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        topic TEXT,
        semester TEXT,
        uploaded_by TEXT,
        file_name TEXT,
        description TEXT,
        upload_date TEXT,
        downloads INTEGER DEFAULT 0,
        rating REAL DEFAULT 0.0
    )''')
    conn.commit()
    conn.close()

_init_db()

def add_note(note: Dict) -> int:
    """Add a note to the database. Returns new note id."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO notes (
        subject, topic, semester, uploaded_by, file_name, description, upload_date, downloads, rating
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        note['subject'], note['topic'], note['semester'], note['uploaded_by'], note['file_name'],
        note['description'], note.get('upload_date', datetime.now().strftime('%Y-%m-%d')),
        note.get('downloads', 0), note.get('rating', 0.0)
    ))
    note_id = c.lastrowid
    conn.commit()
    conn.close()
    return note_id

def get_all_notes() -> List[Dict]:
    """Get all notes from the database."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    rows = c.fetchall()
    conn.close()
    keys = ['id', 'subject', 'topic', 'semester', 'uploaded_by', 'file_name', 'description', 'upload_date', 'downloads', 'rating']
    return [dict(zip(keys, row)) for row in rows]

def get_notes_by_subject(subject: str) -> List[Dict]:
    """Get all notes for a given subject."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM notes WHERE subject = ?', (subject,))
    rows = c.fetchall()
    conn.close()
    keys = ['id', 'subject', 'topic', 'semester', 'uploaded_by', 'file_name', 'description', 'upload_date', 'downloads', 'rating']
    return [dict(zip(keys, row)) for row in rows]

def get_note_by_id(note_id: int) -> Optional[Dict]:
    """Get a single note by id."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    row = c.fetchone()
    conn.close()
    if row:
        keys = ['id', 'subject', 'topic', 'semester', 'uploaded_by', 'file_name', 'description', 'upload_date', 'downloads', 'rating']
        return dict(zip(keys, row))
    return None

def increment_download(note_id: int):
    """Increment the download count for a note."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('UPDATE notes SET downloads = downloads + 1 WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()

def update_rating(note_id: int, new_rating: float):
    """Update the rating for a note."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('UPDATE notes SET rating = ? WHERE id = ?', (new_rating, note_id))
    conn.commit()
    conn.close()

def delete_note(note_id: int) -> bool:
    """Delete a note from the database. Returns True if deleted, False if not found."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    deleted = c.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_notes_count_by_user(uploaded_by: str) -> int:
    """Get the actual count of notes uploaded by a specific user."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM notes WHERE uploaded_by = ?', (uploaded_by,))
    count = c.fetchone()[0]
    conn.close()
    return count


# Counter for generating new IDs
note_id_counter = 6

def get_next_note_id() -> int:
    """Generate next unique ID for notes"""
    global note_id_counter
    current_id = note_id_counter
    note_id_counter += 1
    return current_id
"""
Services package - Business logic layer
"""

from .lost_found_service import (
    add_lost_item,
    add_found_item,
    get_all_items,
    get_lost_items,
    get_found_items,
    find_potential_matches,
    claim_item,
    get_item_by_id
)

from .notes_service import (
    upload_note,
    get_notes_by_subject,
    get_all_notes_list,
    increment_download_count,
    get_top_contributors,
    search_notes
)

from .analytics_service import (
    get_lost_found_stats,
    get_notes_stats,
    get_category_distribution,
    get_top_downloaded_notes
)

__all__ = [
    'add_lost_item', 'add_found_item', 'get_all_items', 'get_lost_items', 
    'get_found_items', 'find_potential_matches', 'claim_item', 'get_item_by_id',
    'upload_note', 'get_notes_by_subject', 'get_all_notes_list', 
    'increment_download_count', 'get_top_contributors', 'search_notes',
    'get_lost_found_stats', 'get_notes_stats', 'get_category_distribution',
    'get_top_downloaded_notes'
]
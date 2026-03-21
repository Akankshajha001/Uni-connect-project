"""
Notes Exchange UI - User interface for notes sharing
"""

import streamlit as st
st.markdown(
    """
    <style>
    /* Make all Streamlit form labels dark and bold */
    label, .stTextInput label, .stSelectbox label, .stTextArea label, .css-1c7y2kd, .css-1n76uvr {
        color: #222 !important;
        font-weight: 700 !important;
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
from services.notes_service import (
    upload_note,
    get_notes_by_subject,
    get_subjects,
    get_all_notes_list,
    increment_download_count,
    get_top_contributors,
    search_notes,
    get_recent_notes,
    get_popular_notes
)
from database.users_db import update_user_activity
from utils.helpers import format_date, format_number, truncate_text
from utils.validators import validate_name, validate_file_name, validate_description

# Semesters
SEMESTERS = ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 
             'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8']

def render_notes_exchange():
    """Main render function for Notes Exchange section"""
    
    # Check if user is logged in
    if 'user' not in st.session_state or st.session_state.user is None:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; border-radius: 15px; color: white; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
                <h1 style='margin: 0; font-size: 2.5rem;'>📚 Notes Exchange Center</h1>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                    Share knowledge, excel together
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.error("🔒 Please login from the sidebar to access the Notes Exchange section.")
        
        st.markdown("""
            <div style='background: #f8d7da; padding: 2rem; border-radius: 15px; 
                        border-left: 5px solid #f5576c; margin-top: 2rem;'>
                <h3 style='margin: 0; color: #721c24;'>📝 Login Required</h3>
                <p style='margin: 0.5rem 0 0 0; color: #721c24;'>
                    To upload or download notes, please sign in using the form in the sidebar.
                    Join our community of knowledge sharers today!
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem; border-radius: 15px; color: white; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2.5rem;'>📚 Notes Exchange Center</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                Share knowledge, excel together
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Upload Notes",
        "📥 Browse All",
        "🔥 Popular",
        "🔍 Search",
        "🏆 Contributors"
    ])
    
    with tab1:
        render_upload_notes()
    
    with tab2:
        render_browse_notes()
    
    with tab3:
        render_popular_notes()
    
    with tab4:
        render_search_notes()
    
    with tab5:
        render_contributors()

def render_upload_notes():
    """Form to upload new notes"""
    st.markdown("### 📤 Upload Your Notes")
    st.markdown("Share your notes with fellow students and help them succeed!")
    
    with st.form("upload_notes_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input(
                "Subject Name *",
                placeholder="e.g., Data Structures",
                help="Enter the subject name"
            )
            
            semester = st.selectbox(
                "Semester *",
                options=SEMESTERS,
                help="Which semester is this for?"
            )
        
        with col2:
            user = st.session_state.user if 'user' in st.session_state and st.session_state.user else {}
            uploaded_by = st.text_input(
                "Your Name *",
                placeholder="e.g., John Doe",
                value=user.get('name', ''),
                help="Your name will be credited"
            )
            
            # File uploader for PDF, DOCX, TXT files
            uploaded_file = st.file_uploader(
                "Upload File *",
                type=["pdf", "doc", "docx", "txt"],
                help="Upload your notes file (PDF, DOC, DOCX, or TXT)",
                key="notes_file_uploader"
            )
        
        description = st.text_area(
            "Description *",
            placeholder="Describe the content: topics covered, diagrams, examples, etc.",
            height=100,
            help="Help others understand what's in your notes"
        )
        
        submit = st.form_submit_button("🚀 Upload Notes", use_container_width=True)
        
        if submit:
            # Validate inputs
            if not all([subject, semester, uploaded_by, uploaded_file, description]):
                st.error("❌ Please fill all required fields and upload a file")
            else:
                # Validate name
                name_valid, name_error = validate_name(uploaded_by)
                if not name_valid:
                    st.error(f"❌ {name_error}")
                    return
                
                # Get file name from uploaded file
                file_name = uploaded_file.name
                file_size = uploaded_file.size
                
                # Auto-generate topic from filename (without extension)
                topic = file_name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ')
                
                # Validate file size (max 10MB)
                if file_size > 10 * 1024 * 1024:
                    st.error("❌ File size too large. Maximum 10MB allowed.")
                    return
                
                # Validate description
                desc_valid, desc_error = validate_description(description)
                if not desc_valid:
                    st.error(f"❌ {desc_error}")
                    return
                
                # Save uploaded file
                import os
                upload_dir = "uploaded_notes"
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                file_path = os.path.join(upload_dir, file_name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Upload note with file path
                note = upload_note(
                    subject=subject,
                    topic=topic,
                    semester=semester,
                    uploaded_by=uploaded_by,
                    file_name=file_name,
                    description=description
                )
                
                update_user_activity(st.session_state.user['id'], 'note_uploaded')
                
                st.success("✅ Notes uploaded successfully!")
                st.balloons()
                
                # Show file info
                st.markdown(f"""
                    <div style='background: #e3f2fd; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                        <p style='margin: 0; color: #1565c0;'>
                            <strong>📄 File Uploaded:</strong> {file_name}<br>
                            <strong>📦 File Size:</strong> {round(file_size / 1024, 2)} KB<br>
                            <strong>📁 File Type:</strong> {file_name.split('.')[-1].upper()}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style='background: #e8f5e9; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                        <p style='margin: 0; color: #2e7d32;'>
                            <strong>Note ID:</strong> {note['id']}<br>
                            <strong>Subject:</strong> {note['subject']}<br>
                            <strong>Status:</strong> Published - Students can now access your notes!
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Show contribution stats
                contributors = get_top_contributors()
                user_contrib = next((c for c in contributors if c['name'] == uploaded_by), None)
                if user_contrib:
                    st.markdown(f"""
                        <div style='background: #fff3e0; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                            <p style='margin: 0; color: #e65100;'>
                                🎉 <strong>Your Contribution Stats:</strong><br>
                                Total Uploads: {user_contrib['uploads']} | 
                                Total Downloads: {user_contrib['total_downloads']} | 
                                Subjects: {len(user_contrib['subjects'])}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

def render_browse_notes():
    """Browse notes by subject"""
    st.markdown("### 📥 Browse All Notes")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        subjects = get_subjects()
        selected_subject = st.selectbox(
            "Filter by Subject",
            options=["All Subjects"] + subjects,
            key="browse_subject_filter"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=["Most Recent", "Most Downloaded", "Subject Name"],
            key="browse_sort"
        )
    
    # Get notes
    if selected_subject == "All Subjects":
        notes = get_all_notes_list()
    else:
        notes = get_notes_by_subject(selected_subject)
    
    # Sort notes
    if sort_by == "Most Recent":
        notes = sorted(notes, key=lambda x: x['upload_date'], reverse=True)
    elif sort_by == "Most Downloaded":
        notes = sorted(notes, key=lambda x: x['downloads'], reverse=True)
    else:  # Subject Name
        notes = sorted(notes, key=lambda x: x['subject'])
    
    if not notes:
        st.info("No notes found. Be the first to upload!")
    else:
        st.success(f"Found {len(notes)} note(s)")
        
        # Display notes in a grid
        cols_per_row = 2
        for i in range(0, len(notes), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(notes):
                    with col:
                        render_note_card(notes[i + j], context='browse')

def render_popular_notes():
    """Display popular/trending notes"""
    st.markdown("### 🔥 Popular Notes")
    st.markdown("Most downloaded notes by your peers")
    
    popular = get_popular_notes(limit=12)
    
    if not popular:
        st.info("No notes available yet.")
    else:
        # Display in grid
        cols_per_row = 2
        for i in range(0, len(popular), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(popular):
                    with col:
                        render_note_card(popular[i + j], show_popularity=True, context='popular')

def render_search_notes():
    """Search notes"""
    st.markdown("### 🔍 Search Notes")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Search by subject, topic, or uploader",
            placeholder="e.g., database, sorting algorithms, John...",
            key="search_notes_query"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", use_container_width=True)
    
    if search_query or search_btn:
        results = search_notes(search_query) if search_query else get_all_notes_list()
        
        if not results:
            st.info("No notes found matching your search.")
        else:
            st.success(f"Found {len(results)} note(s)")
            
            # Display results
            cols_per_row = 2
            for i in range(0, len(results), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(results):
                        with col:
                            render_note_card(results[i + j], context='search')

def render_contributors():
    """Display top contributors leaderboard"""
    st.markdown("### 🏆 Top Contributors")
    st.markdown("Celebrating students who share their knowledge!")
    
    contributors = get_top_contributors(limit=20)
    
    if not contributors:
        st.info("No contributors yet. Be the first!")
    else:
        # Podium for top 3
        if len(contributors) >= 3:
            st.markdown("#### 🥇🥈🥉 Top 3 Contributors")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                render_contributor_podium(contributors[0], "🥇", "#FFD700")
            with col2:
                render_contributor_podium(contributors[1], "🥈", "#C0C0C0")
            with col3:
                render_contributor_podium(contributors[2], "🥉", "#CD7F32")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Rest of contributors in table
        if len(contributors) > 3:
            st.markdown("#### 📊 All Contributors")
            
            for i, contributor in enumerate(contributors):
                rank = i + 1
                
                # Medal for top 3
                if rank == 1:
                    medal = "🥇"
                elif rank == 2:
                    medal = "🥈"
                elif rank == 3:
                    medal = "🥉"
                else:
                    medal = f"#{rank}"
                
                st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 1rem; border-radius: 10px; 
                                margin-bottom: 0.5rem; border-left: 4px solid #667eea;'>
                        <span style='font-size: 1.2rem; font-weight: bold;'>{medal}</span>
                        <strong style='margin-left: 1rem;'>{contributor['name']}</strong>
                        <span style='float: right; color: #666;'>
                            📤 {contributor['uploads']} uploads | 
                            📥 {contributor['total_downloads']} downloads | 
                            📚 {len(contributor['subjects'])} subjects
                        </span>
                    </div>
                """, unsafe_allow_html=True)

def render_contributor_podium(contributor, medal, color):
    """Render podium card for top contributor"""
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}40 0%, {color}20 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center;
                    border: 3px solid {color}; box-shadow: 0 5px 20px rgba(0,0,0,0.2);'>
            <div style='font-size: 3rem;'>{medal}</div>
            <h3 style='margin: 0.5rem 0; color: #333;'>{contributor['name']}</h3>
            <p style='margin: 0.5rem 0; color: #666; font-size: 1.1rem;'>
                <strong>{contributor['uploads']}</strong> uploads
            </p>
            <p style='margin: 0; color: #666;'>
                {contributor['total_downloads']} downloads
            </p>
            <p style='margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;'>
                {len(contributor['subjects'])} subjects
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_note_card(note, show_popularity=False, context='default'):
    """Render a single note card"""
    date_text = format_date(note['upload_date'], 'display')
    downloads_text = format_number(note['downloads'])
    
    # Determine file icon based on extension
    file_name = note.get('file_name', '')
    file_ext = file_name.split('.')[-1].lower() if '.' in file_name else 'file'
    
    file_icons = {
        'pdf': '📕',
        'doc': '📘',
        'docx': '📘',
        'txt': '📝',
        'ppt': '📊',
        'pptx': '📊',
        'xls': '📊',
        'xlsx': '📊'
    }
    file_icon = file_icons.get(file_ext, '📄')
    
    # Create a nice card with all information
    card_html = f"""
    <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                margin-bottom: 1rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;'>
        <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
            <span style='font-size: 2rem; margin-right: 0.5rem;'>{file_icon}</span>
            <div style='flex-grow: 1;'>
                <h4 style='margin: 0; color: #1e88e5; font-size: 1.1rem;'>{note['topic']}</h4>
                <span style='background: #e3f2fd; color: #1565c0; padding: 0.2rem 0.5rem; 
                             border-radius: 5px; font-size: 0.75rem;'>{file_ext.upper()}</span>
            </div>
        </div>
        <p style='margin: 0.5rem 0; color: #666; font-size: 0.9rem;'>
            <strong>{note['subject']}</strong> • {note['semester']}
        </p>
        <p style='margin: 0.5rem 0; color: #444; font-size: 0.95rem;'>
            {truncate_text(note['description'], 100)}
        </p>
        <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee;'>
            <p style='margin: 0; color: #888; font-size: 0.85rem;'>
                👤 {note['uploaded_by']}<br>
                📅 {date_text} • 📥 {downloads_text} downloads
            </p>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Download button
    col1, col2 = st.columns(2)
    with col1:
        # Check if file exists
        import os
        file_path = os.path.join("uploaded_notes", note['file_name'])
        
        if os.path.exists(file_path):
            # Read file for download
            with open(file_path, "rb") as file:
                file_data = file.read()
            
            if st.download_button(
                label="📥 Download",
                data=file_data,
                file_name=note['file_name'],
                mime="application/octet-stream",
                key=f"download_{context}_{note['id']}",
                use_container_width=True
            ):
                increment_download_count(note['id'])
                update_user_activity(st.session_state.user['id'], 'note_downloaded')
        else:
            # For sample data that doesn't have actual files
            if st.button(f"📥 Download", key=f"download_{context}_{note['id']}", use_container_width=True):
                increment_download_count(note['id'])
                update_user_activity(st.session_state.user['id'], 'note_downloaded')
                st.info(f"ℹ️ Sample file: {note['file_name']} (Demo mode - actual file not available)")
    
    with col2:
        if st.button(f"ℹ️ Details", key=f"details_{context}_{note['id']}", use_container_width=True):
            st.session_state[f'show_details_{context}_{note["id"]}'] = True
    
    # Show details if button clicked
    if st.session_state.get(f'show_details_{context}_{note["id"]}', False):
        with st.expander("📋 Full Details", expanded=True):
            st.markdown(f"""
                **Note ID:** {note['id']}  
                **Subject:** {note['subject']}  
                **Topic:** {note['topic']}  
                **Semester:** {note['semester']}  
                **File Name:** {note['file_name']}  
                **Uploaded By:** {note['uploaded_by']}  
                **Upload Date:** {date_text}  
                **Downloads:** {note['downloads']}  
                **Rating:** {'⭐' * int(note.get('rating', 0))} ({note.get('rating', 0)})  
                
                **Description:**  
                {note['description']}
            """)
            
            if st.button("❌ Close", key=f"close_details_{context}_{note['id']}"):
                st.session_state[f'show_details_{context}_{note["id"]}'] = False
                st.rerun()
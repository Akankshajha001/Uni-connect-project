"""
Uni-Connect - Main Application Entry Point
A Streamlit-based platform for Lost & Found and Notes Exchange

Description: Campus utility platform using in-memory Python data structures
"""

import streamlit as st
from database.users_db import signup_user, login_user, get_user_by_id
from ui.dashboard_ui import render_dashboard
from ui.lost_found_ui import render_lost_found
from ui.notes_ui import render_notes_exchange
from utils.validators import validate_name, validate_email, validate_roll_no


def load_custom_css():
    """Inject custom CSS for the app (placeholder)."""
    st.markdown("""
        <style>
        /* Example: Make sidebar background dark */
        .css-1d391kg { background: #222 !important; }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with navigation and user info"""
    with st.sidebar:
        # Logo and Title
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0; color: white;'>
                <h1 style='font-size: 2.5rem; margin: 0;'>🎓</h1>
                <h2 style='margin: 0.5rem 0; font-size: 1.5rem;'>Uni-Connect</h2>
                <p style='margin: 0; opacity: 0.8; font-size: 0.9rem;'>Connect • Share • Succeed</p>
            </div>
            <hr style='border: 1px solid rgba(255,255,255,0.3); margin: 1rem 0;'>
        """, unsafe_allow_html=True)

        # User session state
        if 'user' not in st.session_state:
            st.session_state.user = None

        if st.session_state.user is None:
            tabs = st.tabs(["Login", "Sign Up"])
            with tabs[0]:
                st.markdown("<h3 style='color: white;'>👤 Login</h3>", unsafe_allow_html=True)
                with st.form("sidebar_login_form"):
                    email = st.text_input("Email", placeholder="your.email@example.com")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
                    if login_btn:
                        email_valid, email_error = validate_email(email)
                        if not email_valid:
                            st.error(email_error)
                        else:
                            user = login_user(email, password)
                            if user:
                                st.session_state.user = user
                                st.success(f"Welcome, {user['name']}! 🎉")
                                st.rerun()
                            else:
                                st.error("Invalid email or password.")
            with tabs[1]:
                st.markdown("<h3 style='color: white;'>📝 Sign Up</h3>", unsafe_allow_html=True)
                with st.form("sidebar_signup_form"):
                    name = st.text_input("Name", placeholder="Enter your name")
                    roll_no = st.text_input("Roll Number", placeholder="e.g., 2021-CS-001")
                    email = st.text_input("Email", placeholder="your.email@example.com")
                    password = st.text_input("Password", type="password", placeholder="Create a password")
                    signup_btn = st.form_submit_button("📝 Sign Up", use_container_width=True)
                    if signup_btn:
                        name_valid, name_error = validate_name(name)
                        roll_valid, roll_error = validate_roll_no(roll_no)
                        email_valid, email_error = validate_email(email)
                        if not name_valid:
                            st.error(name_error)
                        elif not roll_valid:
                            st.error(roll_error)
                        elif not email_valid:
                            st.error(email_error)
                        elif not password or len(password) < 6:
                            st.error("Password must be at least 6 characters.")
                        else:
                            success = signup_user(name, roll_no, email, password)
                            if success:
                                st.success("Signup successful! Please login.")
                            else:
                                st.error("Email or roll number already exists.")
        else:
            user = st.session_state.user
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; 
                            border-radius: 10px; color: white; margin-bottom: 1rem;'>
                    <h3 style='margin: 0; font-size: 1.2rem;'>👤 {user['name']}</h3>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;'>
                        Email: {user['email']}<br>
                        Roll: {user['roll_no']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.success("Logged out successfully!")
                st.rerun()

        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # Navigation
        st.markdown("""
            <div style='color: white; padding: 0.5rem 0;'>
                <h3 style='margin: 0; font-size: 1.2rem;'>📍 Navigation</h3>
            </div>
        """, unsafe_allow_html=True)

        # Initialize page state if not exists
        if 'page' not in st.session_state:
            st.session_state.page = 'dashboard'

        # Navigation Buttons with custom styling
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏠", help="Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        
        with col2:
            if st.button("🔍", help="Lost & Found", use_container_width=True):
                st.session_state.page = 'lost_found'
                st.rerun()
        
        with col3:
            if st.button("📚", help="Notes", use_container_width=True):
                st.session_state.page = 'notes'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Full width navigation buttons
        if st.button("🏠 Dashboard", use_container_width=True, 
                     type="primary" if st.session_state.page == 'dashboard' else "secondary"):
            st.session_state.page = 'dashboard'
            st.rerun()
        
        if st.button("🔍 Lost & Found", use_container_width=True,
                     type="primary" if st.session_state.page == 'lost_found' else "secondary"):
            st.session_state.page = 'lost_found'
            st.rerun()
        
        if st.button("📚 Notes Exchange", use_container_width=True,
                     type="primary" if st.session_state.page == 'notes' else "secondary"):
            st.session_state.page = 'notes'
            st.rerun()
        
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div style='text-align: center; color: white; opacity: 0.6; 
                        font-size: 0.8rem; padding: 1rem 0;'>
                <p style='margin: 0;'>Uni-Connect v2.0</p>
                <p style='margin: 0;'>Made with ❤️ using Streamlit</p>
                <p style='margin: 0;'>© 2026 - All rights reserved</p>
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Load custom CSS
    load_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    # Get current page from session state
    current_page = st.session_state.get('page', 'dashboard')
    
    # Render appropriate page
    if current_page == 'dashboard':
        render_dashboard()
    elif current_page == 'lost_found':
        render_lost_found()
    elif current_page == 'notes':
        render_notes_exchange()
    else:
        # Default to dashboard
        render_dashboard()

if __name__ == "__main__":
    main()
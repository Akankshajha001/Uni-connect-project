"""
Lost & Found UI - User interface for lost and found items
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
import os
from datetime import datetime
from services.lost_found_service import (
    add_lost_item,
    add_found_item,
    get_all_items,
    get_lost_items,
    get_found_items,
    find_potential_matches,
    claim_item,
    search_items
)
from database.users_db import update_user_activity
from utils.helpers import format_date, get_date_difference, truncate_text
from utils.validators import validate_name, validate_description

# Categories for items
CATEGORIES = ['ID Card', 'Bottle', 'Charger', 'Book', 'Umbrella', 'Keys', 
              'Phone', 'Wallet', 'Bag', 'Laptop', 'Headphones', 'Other']

# Common locations on campus
LOCATIONS = ['Library', 'Cafeteria', 'Computer Lab', 'Main Building', 
             'Sports Complex', 'Auditorium', 'Parking Area', 'Garden', 
             'Hostel Area', 'Other']

def render_lost_found():
    """Main render function for Lost & Found section"""
    
    # Check if user is logged in
    if 'user' not in st.session_state or st.session_state.user is None:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
                <h1 style='margin: 0; font-size: 2.5rem;'>🔍 Lost & Found Center</h1>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                    Help reunite items with their owners
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.error("🔒 Please login from the sidebar to access the Lost & Found section.")
        
        st.markdown("""
            <div style='background: #fff3cd; padding: 2rem; border-radius: 15px; 
                        border-left: 5px solid #ffc107; margin-top: 2rem;'>
                <h3 style='margin: 0; color: #856404;'>📝 Login Required</h3>
                <p style='margin: 0.5rem 0 0 0; color: #856404;'>
                    To report lost or found items, please sign in using the form in the sidebar.
                    It's quick and easy - just enter your name, roll number, and email!
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2.5rem;'>🔍 Lost & Found Center</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                Help reunite items with their owners
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📢 Report Lost", 
        "✅ Report Found", 
        "🔎 Search Items", 
        "📋 All Items"
    ])
    
    with tab1:
        render_report_lost()
    
    with tab2:
        render_report_found()
    
    with tab3:
        render_search_items()
    
    with tab4:
        render_all_items()

def render_report_lost():
    """Form to report a lost item"""
    st.markdown("### 📢 Report a Lost Item")
    st.markdown("Help us help you find your lost item by providing detailed information.")
    
    st.markdown("""
        <div style='background: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 4px solid #2196f3;'>
            <p style='margin: 0; color: #1565c0;'>
                ℹ️ <strong>Note:</strong> You will receive a unique <strong>5-digit verification code</strong> 
                after submitting. Keep it safe - you'll need to share it with anyone claiming your item!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("report_lost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Category *",
                options=CATEGORIES,
                help="Select the category that best describes your item"
            )
            
            location = st.selectbox(
                "Last Seen Location *",
                options=LOCATIONS,
                help="Where did you last see your item?"
            )
        
        with col2:
            user = st.session_state.user if 'user' in st.session_state and st.session_state.user else {}
            reporter_name = st.text_input(
                "Your Name *",
                placeholder="e.g., John Doe",
                value=user.get('name', '')
            )
            
            reporter_contact = st.text_input(
                "Contact (Email/Phone) *",
                placeholder="e.g., john@example.com",
                value=user.get('email', '')
            )
        
        description = st.text_area(
            "Description *",
            placeholder="Provide detailed description: color, brand, distinguishing features, specific name, etc.",
            height=100,
            help="More details increase the chance of finding your item"
        )
        
        st.markdown("<h4 style='color: #333; margin-top: 1rem;'>📸 Optional: Upload Image</h4>", unsafe_allow_html=True)
        image_file = st.file_uploader(
            "Upload image of the item (optional)",
            type=['png', 'jpg', 'jpeg'],
            help="A photo helps others identify your item more easily",
            label_visibility="collapsed"
        )
        
        submit = st.form_submit_button("🚀 Submit Lost Item Report", use_container_width=True)
        
        if submit:
            # Validate inputs
            if not all([category, location, reporter_name, reporter_contact, description]):
                st.error("❌ Please fill all required fields marked with *")
            else:
                # Validate name
                name_valid, name_error = validate_name(reporter_name)
                if not name_valid:
                    st.error(f"❌ {name_error}")
                    return
                
                # Validate description
                desc_valid, desc_error = validate_description(description)
                if not desc_valid:
                    st.error(f"❌ {desc_error}")
                    return
                
                # Handle image upload
                image_path = None
                if image_file is not None:
                    # Create directory if it doesn't exist
                    image_dir = "uploaded_images"
                    os.makedirs(image_dir, exist_ok=True)
                    
                    # Save image with unique name
                    image_path = os.path.join(image_dir, f"lost_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}")
                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                
                # Add item (use category as item_name)
                item = add_lost_item(
                    item_name=category,
                    category=category,
                    location=location,
                    description=description,
                    reporter_name=reporter_name,
                    reporter_contact=reporter_contact,
                    image_path=image_path
                )
                
                update_user_activity(st.session_state.user['id'], 'item_reported')
                
                st.success("✅ Lost item reported successfully!")
                st.balloons()
                
                # Show potential matches
                matches = find_potential_matches('lost', category, location)
                if matches:
                    st.info(f"🎯 Found {len(matches)} potential match(es)! Check the 'Search Items' tab.")
                
                st.markdown(f"""
                    <div style='background: #fff3cd; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;
                                border-left: 5px solid #ffc107; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                        <h4 style='margin: 0 0 1rem 0; color: #856404;'>🔑 Important - Save This Information!</h4>
                        <p style='margin: 0; color: #856404; font-size: 1.1rem;'>
                            <strong>Item ID:</strong> #{item['id']}<br>
                            <strong>Verification Code:</strong> <span style='font-size: 1.5rem; font-weight: bold; 
                            background: #ffc107; padding: 5px 15px; border-radius: 5px; color: white;'>{item['verification_code']}</span><br>
                            <strong>Status:</strong> Open<br><br>
                            <span style='font-size: 0.9rem;'>⚠️ Keep this verification code safe! You'll need it when someone claims your item.</span>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

def render_report_found():
    """Form to report a found item"""
    st.markdown("### ✅ Report a Found Item")
    st.markdown("Help someone recover their lost item by reporting what you found.")
    
    st.markdown("""
        <div style='background: #e8f5e9; padding: 1rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 4px solid #4caf50;'>
            <p style='margin: 0; color: #2e7d32;'>
                ℹ️ <strong>Note:</strong> You will receive a unique <strong>5-digit verification code</strong> 
                after submitting. Share this code with the owner when they claim the item!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("report_found_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Category *",
                options=CATEGORIES,
                help="Select the category"
            )
            
            location = st.selectbox(
                "Found Location *",
                options=LOCATIONS,
                help="Where did you find this item?"
            )
        
        with col2:
            user = st.session_state.user if 'user' in st.session_state and st.session_state.user else {}
            reporter_name = st.text_input(
                "Your Name *",
                placeholder="e.g., Jane Smith",
                value=user.get('name', '')
            )
            
            reporter_contact = st.text_input(
                "Contact (Email/Phone) *",
                placeholder="e.g., jane@example.com",
                value=user.get('email', '')
            )
        
        description = st.text_area(
            "Description *",
            placeholder="Describe the item in detail so the owner can identify it: color, brand, specific features, etc.",
            height=100,
            help="Detailed description helps the rightful owner claim it"
        )
        
        st.markdown("<h4 style='color: #333; margin-top: 1rem;'>📸 Optional: Upload Image</h4>", unsafe_allow_html=True)
        image_file = st.file_uploader(
            "Upload image of the item (optional)",
            type=['png', 'jpg', 'jpeg'],
            help="A photo helps the owner identify their item",
            label_visibility="collapsed",
            key="found_image"
        )
        
        submit = st.form_submit_button("✅ Submit Found Item Report", use_container_width=True)
        
        if submit:
            # Validate inputs
            if not all([category, location, reporter_name, reporter_contact, description]):
                st.error("❌ Please fill all required fields marked with *")
            else:
                # Validate name
                name_valid, name_error = validate_name(reporter_name)
                if not name_valid:
                    st.error(f"❌ {name_error}")
                    return
                
                # Validate description
                desc_valid, desc_error = validate_description(description)
                if not desc_valid:
                    st.error(f"❌ {desc_error}")
                    return
                
                # Handle image upload
                image_path = None
                if image_file is not None:
                    # Create directory if it doesn't exist
                    image_dir = "uploaded_images"
                    os.makedirs(image_dir, exist_ok=True)
                    
                    # Save image with unique name
                    image_path = os.path.join(image_dir, f"found_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}")
                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                
                # Add item (use category as item_name)
                item = add_found_item(
                    item_name=category,
                    category=category,
                    location=location,
                    description=description,
                    reporter_name=reporter_name,
                    reporter_contact=reporter_contact,
                    image_path=image_path
                )
                
                update_user_activity(st.session_state.user['id'], 'item_reported')
                
                st.success("✅ Found item reported successfully!")
                st.balloons()
                
                # Show potential matches
                matches = find_potential_matches('found', category, location)
                if matches:
                    st.info(f"🎯 This might match {len(matches)} lost item(s)! Check the 'Search Items' tab.")
                
                st.markdown(f"""
                    <div style='background: #e3f2fd; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;
                                border-left: 5px solid #2196f3; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                        <h4 style='margin: 0 0 1rem 0; color: #1565c0;'>🔑 Important - Save This Information!</h4>
                        <p style='margin: 0; color: #1565c0; font-size: 1.1rem;'>
                            <strong>Item ID:</strong> #{item['id']}<br>
                            <strong>Verification Code:</strong> <span style='font-size: 1.5rem; font-weight: bold; 
                            background: #2196f3; padding: 5px 15px; border-radius: 5px; color: white;'>{item['verification_code']}</span><br>
                            <strong>Status:</strong> Open<br><br>
                            <span style='font-size: 0.9rem;'>⚠️ Share this verification code with the owner when they claim the item!</span>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

def render_search_items():
    """Search and view matching items"""
    st.markdown("### 🔎 Search Items")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Search by item name, category, or location",
            placeholder="e.g., bottle, ID card, library...",
            key="search_items"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", use_container_width=True)
    
    if search_query or search_btn:
        results = search_items(search_query) if search_query else get_all_items()
        
        if not results:
            st.info("No items found matching your search.")
        else:
            st.success(f"Found {len(results)} item(s)")
            
            # Separate lost and found
            lost_results = [item for item in results if item['type'] == 'lost']
            found_results = [item for item in results if item['type'] == 'found']
            
            if lost_results:
                st.markdown("#### 📢 Lost Items")
                for item in lost_results:
                    render_item_card(item, context='search_lost')
            
            if found_results:
                st.markdown("#### ✅ Found Items")
                for item in found_results:
                    render_item_card(item, context='search_found')

def render_all_items():
    """Display all items with filters"""
    st.markdown("### 📋 All Items")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Filter by Type", ["All", "Lost", "Found"])
    with col2:
        filter_category = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
    with col3:
        filter_status = st.selectbox("Filter by Status", ["All", "Open", "Claimed"])
    
    # Get items based on filter
    if filter_type == "Lost":
        items = get_lost_items()
    elif filter_type == "Found":
        items = get_found_items()
    else:
        items = get_all_items()
    
    # Apply category filter
    if filter_category != "All":
        items = [item for item in items if item['category'] == filter_category]
    
    # Apply status filter
    if filter_status != "All":
        items = [item for item in items if item['status'].lower() == filter_status.lower()]
    
    if not items:
        st.info("No items found with the selected filters.")
    else:
        st.success(f"Showing {len(items)} item(s)")
        
        # Sort by date (most recent first)
        items_sorted = sorted(items, key=lambda x: x['date'], reverse=True)
        
        for item in items_sorted:
            render_item_card(item, context='all_items')

def render_item_card(item, context='default'):
    """Render a single item card
    
    Args:
        item: The item dictionary to render
        context: A unique identifier for where this card is being rendered (e.g., 'search', 'all', 'lost', 'found')
    """
    # Determine color based on type and status
    if item['status'] == 'claimed':
        border_color = '#4caf50'
        status_emoji = '✅'
    elif item['type'] == 'lost':
        border_color = '#f44336'
        status_emoji = '📢'
    else:
        border_color = '#2196f3'
        status_emoji = '✅'
    
    days_ago = get_date_difference(item['date'])
    date_text = format_date(item['date'], 'display')
    
    # Show image if available
    if item.get('image_path'):
        try:
            import os
            if os.path.exists(item['image_path']):
                col_img, col_details = st.columns([1, 3])
                with col_img:
                    st.image(item['image_path'], use_container_width=True, caption="Item Image")
                with col_details:
                    st.markdown(f"""
                        <div style='border-left: 5px solid {border_color}; padding: 1rem; 
                                    background: #f8f9fa; border-radius: 10px;
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                            <h4 style='margin: 0; color: #333;'>
                                {status_emoji} {item['item_name']}
                                <span style='float: right; font-size: 0.8rem; color: #666;'>
                                    ID: #{item['id']}
                                </span>
                            </h4>
                            <p style='margin: 0.5rem 0; color: #666;'>
                                <strong>Category:</strong> {item['category']} | 
                                <strong>Location:</strong> {item['location']} | 
                                <strong>Status:</strong> {item['status'].title()}
                            </p>
                            <p style='margin: 0.5rem 0; color: #444;'>
                                {item['description']}
                            </p>
                            <p style='margin: 0.5rem 0 0 0; color: #888; font-size: 0.9rem;'>
                                <strong>Reported by:</strong> {item['reporter_name']} | 
                                <strong>Contact:</strong> {item['reporter_contact']} | 
                                <strong>Date:</strong> {date_text} ({days_ago} days ago)
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
        except:
            pass
    
    # No image or image failed to load - show regular card
    if not item.get('image_path') or not os.path.exists(item.get('image_path', '')):
        st.markdown(f"""
            <div style='border-left: 5px solid {border_color}; padding: 1rem; 
                        background: #f8f9fa; border-radius: 10px; margin-bottom: 1rem;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; color: #333;'>
                    {status_emoji} {item['item_name']}
                    <span style='float: right; font-size: 0.8rem; color: #666;'>
                        ID: #{item['id']}
                    </span>
                </h4>
                <p style='margin: 0.5rem 0; color: #666;'>
                    <strong>Category:</strong> {item['category']} | 
                    <strong>Location:</strong> {item['location']} | 
                    <strong>Status:</strong> {item['status'].title()}
                </p>
                <p style='margin: 0.5rem 0; color: #444;'>
                    {item['description']}
                </p>
                <p style='margin: 0.5rem 0 0 0; color: #888; font-size: 0.9rem;'>
                    <strong>Reported by:</strong> {item['reporter_name']} | 
                    <strong>Contact:</strong> {item['reporter_contact']} | 
                    <strong>Date:</strong> {date_text} ({days_ago} days ago)
                </p>
            </div>
        """, unsafe_allow_html=True)
    # Claim button for open items
    if item['status'] == 'open':
        # Check if user is logged in
        if 'user' not in st.session_state or st.session_state.user is None:
            st.warning("⚠️ Please login to claim this item")
        else:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.button(f"🏆 Claim Item #{item['id']}", key=f"claim_{context}_{item['id']}"):
                    st.session_state[f'claiming_{context}_{item["id"]}'] = True
            
            # Show claim form if button clicked
            if st.session_state.get(f'claiming_{context}_{item["id"]}', False):
                user = st.session_state.user
                st.markdown("""
                    <div style='background: #fff3cd; padding: 1rem; border-radius: 10px; 
                                border-left: 4px solid #ffc107; margin: 1rem 0;'>
                        <h4 style='margin: 0; color: #856404;'>🔐 Verify Your Identity & Ownership</h4>
                        <p style='margin: 0.5rem 0 0 0; color: #856404;'>
                            To prevent fraudulent claims, please provide verification details
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                # Show who is claiming
                st.info(f"👤 Claiming as: **{user['name']}** ({user['email']})")
                with st.form(f"claim_form_{context}_{item['id']}"):
                    st.markdown("**Verification Required** ⚠️")
                    st.markdown(f"""
                        <div style='background: #fff3cd; padding: 0.8rem; border-radius: 5px; margin-bottom: 1rem;'>
                            <p style='margin: 0; color: #856404; font-size: 0.9rem;'>
                                📞 <strong>First Step:</strong> Contact <strong>{item['reporter_name']}</strong> at 
                                <strong>{item['reporter_contact']}</strong> to get the verification code!
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    verification_code_input = st.text_input(
                        "5-Digit Verification Code *",
                        max_chars=5,
                        key=f"ver_code_{item['id']}",
                        help="Contact the reporter to get this code",
                        placeholder="12345"
                    )
                    verification = st.text_area(
                        "Proof of Ownership *",
                        placeholder="Describe specific details only the owner would know...",
                        key=f"verification_{item['id']}",
                        help="Examples: exact color, brand/model, contents, unique marks, serial number, when/where purchased, etc.",
                        height=80
                    )
                    contact = st.text_input(
                        "Contact Number *",
                        value=user.get('phone', ''),
                        key=f"contact_{item['id']}",
                        help="Your contact number for verification"
                    )
                    st.markdown("""
                        <div style='background: #e3f2fd; padding: 0.8rem; border-radius: 5px; margin: 1rem 0;'>
                            <p style='margin: 0; color: #1565c0; font-size: 0.9rem;'>
                                ℹ️ <strong>Note:</strong> The item reporter will be notified and may contact you 
                                to verify your claim before releasing the item.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("✅ Confirm Claim", type="primary", use_container_width=True)
                    with col2:
                        cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                    if cancel:
                        st.session_state[f'claiming_{item["id"]}'] = False
                        st.rerun()
                    if submitted:
                        # Validate inputs
                        if not verification_code_input or not verification or not contact:
                            st.error("⚠️ Please fill in all required fields!")
                        elif verification_code_input.strip() != str(item.get('verification_code', '')).strip():
                            st.error(f"❌ Incorrect verification code! Please check with the reporter and try again.")
                            st.info(f"💡 Hint: Contact {item['reporter_name']} ({item['reporter_contact']}) to get the correct code.")
                            # Debug info for testing (remove in production)
                            st.warning(f"🔍 DEBUG: You entered '{verification_code_input.strip()}' but system expected '{item.get('verification_code', '')}' for Item #{item['id']}")
                        elif len(verification.strip()) < 10:
                            st.error("⚠️ Please provide more detailed verification (at least 10 characters)")
                        elif not contact.strip():
                            st.error("⚠️ Please provide a valid contact number!")
                        else:
                            # Submit claim with logged-in user details
                            success = claim_item(
                                item_id=item['id'],
                                claimer_name=user['name'],
                                verification_detail=verification.strip(),
                                claimer_email=user['email'],
                                claimer_contact=contact.strip()
                            )
                            if success:
                                st.success(f"🎉 Claim submitted successfully!")
                                st.markdown(f"""
                                    <div style='background: #d4edda; padding: 1rem; border-radius: 10px; 
                                                border-left: 4px solid #28a745; margin: 1rem 0;'>
                                        <p style='margin: 0; color: #155724;'>
                                            <strong>📧 Next Steps:</strong><br>
                                            • The item reporter (<strong>{item['reporter_name']}</strong>) has been notified<br>
                                            • They will review your verification details<br>
                                            • You will be contacted at <strong>{contact.strip()}</strong><br>
                                            • Please keep your phone accessible
                                        </p>
                                    </div>
                                """, unsafe_allow_html=True)
                                st.balloons()
                                # Update user activity
                                update_user_activity(st.session_state.user['id'], 'claim_item')
                                # Clear claiming state
                                st.session_state[f'claiming_{item["id"]}'] = False
                                # Wait a bit and rerun
                                import time
                                time.sleep(3)
                                st.rerun()
                            else:
                                st.error("❌ Failed to submit claim. Please try again.")
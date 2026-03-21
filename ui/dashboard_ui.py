"""
Dashboard UI - Modern Welcome Page
"""

import streamlit as st

def render_dashboard():
    """Render a stylish modern welcome page"""
    
    # Hero Section with Gradient Background
    st.markdown("""
        <style>
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        .hero-container {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            padding: 4rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 3rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .hero-title {
            color: white;
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            animation: fadeIn 1s ease-out;
        }
        
        .hero-subtitle {
            color: rgba(255,255,255,0.95);
            font-size: 1.5rem;
            margin-bottom: 2rem;
            animation: fadeIn 1.5s ease-out;
        }
        
        .feature-card {
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            animation: fadeIn 2s ease-out;
            height: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        
        .feature-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        
        .feature-title {
            color: #333;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .feature-desc {
            color: #666;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .cta-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2.5rem;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            margin: 1rem 0.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102,126,234,0.4);
        }
        
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102,126,234,0.6);
        }
        
        .benefits-section {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            margin: 3rem 0;
        }
        
        .benefit-item {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .benefit-item:hover {
            transform: scale(1.05);
        }
        </style>
        
        <div class="hero-container">
            <div class="hero-title">
                🎓 Uni-Connect
            </div>
            <div class="hero-subtitle">
                Connecting Students • Sharing Knowledge • Building Community
            </div>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; max-width: 600px; margin: 0 auto;'>
                Your ultimate campus companion for reuniting lost items and exchanging academic resources
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Lost & Found</div>
                <div class="feature-desc">
                    Lost something valuable? Found an item on campus? 
                    Connect with fellow students instantly and reunite belongings with their owners.
                    Our smart matching system helps you find what matters.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">Notes Exchange</div>
                <div class="feature-desc">
                    Share your study materials and access notes from top students.
                    Collaborate, learn together, and excel in your academics.
                    Building a smarter community, one note at a time.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Benefits Section
    st.markdown("""
        <div class="benefits-section">
            <h2 style='text-align: center; color: #333; font-size: 2.5rem; margin-bottom: 2rem;'>
                ✨ Why Choose Uni-Connect?
            </h2>
            <div style='max-width: 800px; margin: 0 auto;'>
                <div class="benefit-item">
                    <strong style='color: #667eea; font-size: 1.3rem;'>🚀 Lightning Fast</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #666;'>
                        Report and search for items in seconds. Our intuitive interface makes everything easy.
                    </p>
                </div>
                <div class="benefit-item">
                    <strong style='color: #f5576c; font-size: 1.3rem;'>🔒 Safe & Secure</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #666;'>
                        Your privacy matters. Only verified students can access the platform.
                    </p>
                </div>
                <div class="benefit-item">
                    <strong style='color: #4facfe; font-size: 1.3rem;'>🤝 Community Driven</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #666;'>
                        Built by students, for students. Help each other succeed and thrive.
                    </p>
                </div>
                <div class="benefit-item">
                    <strong style='color: #43e97b; font-size: 1.3rem;'>📱 Always Available</strong>
                    <p style='margin: 0.5rem 0 0 0; color: #666;'>
                        Access from anywhere, anytime. Your campus resources at your fingertips.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call to Action
    is_logged_in = 'user' in st.session_state and st.session_state.user is not None
    
    if not is_logged_in:
        st.markdown("""
            <div style='text-align: center; padding: 3rem 2rem; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 20px; color: white;'>
                <h2 style='font-size: 2.5rem; margin-bottom: 1rem;'>Ready to Get Started?</h2>
                <p style='font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;'>
                    Join thousands of students already using Uni-Connect
                </p>
                <p style='font-size: 1.1rem;'>
                    👈 Sign up or login from the sidebar to begin your journey
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        user = st.session_state.user
        st.markdown(f"""
            <div style='text-align: center; padding: 3rem 2rem; 
                        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        border-radius: 20px; color: white;'>
                <h2 style='font-size: 2.5rem; margin-bottom: 1rem;'>Welcome back, {user['name']}! 🎉</h2>
                <p style='font-size: 1.2rem; margin-bottom: 2rem;'>
                    What would you like to do today?
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick Action Buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📢 Report Lost Item", use_container_width=True, type="primary"):
                st.session_state.page = 'lost_found'
                st.session_state.lf_action = 'report_lost'
                st.rerun()
        
        with col2:
            if st.button("✅ Report Found Item", use_container_width=True, type="primary"):
                st.session_state.page = 'lost_found'
                st.session_state.lf_action = 'report_found'
                st.rerun()
        
        with col3:
            if st.button("📤 Upload Notes", use_container_width=True, type="primary"):
                st.session_state.page = 'notes'
                st.session_state.notes_action = 'upload'
                st.rerun()
        
        with col4:
            if st.button("📥 Browse Notes", use_container_width=True, type="primary"):
                st.session_state.page = 'notes'
                st.session_state.notes_action = 'browse'
                st.rerun()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 2rem; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    border-radius: 20px; margin-top: 3rem;'>
            <p style='color: #333; margin: 0; font-size: 1.1rem;'>
                💡 <strong>Uni-Connect</strong> - Making campus life easier, one connection at a time
            </p>
            <p style='color: #666; margin: 0.5rem 0 0 0;'>
                Built with ❤️ for students, by students
            </p>
        </div>
    """, unsafe_allow_html=True)
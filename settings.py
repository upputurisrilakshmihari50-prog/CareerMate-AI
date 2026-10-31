import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from database import clear_chat_history, init_db
from utils import load_css, init_session_state

def render_settings_page():
    init_db()
    init_session_state()
    load_css()
    
    user = st.session_state.get("user", {}) or {}
    user_id = user.get("id", st.session_state.get("user_id", 1))
    
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC;">⚙️ Application Settings & Project Credits</h2>
            <p style="color: #94A3B8;">Customize display preferences, manage storage, and view developer credits.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="glass-card">
                <h4 style="color:#38BDF8; margin-top:0;">🎨 UI Theme & Display</h4>
        """, unsafe_allow_html=True)
        
        theme_choice = st.radio("Select Dashboard Theme Accent:", ["Dark Navy (Default)", "Midnight Cyberpunk", "Deep Blue Ocean"], index=0)
        if st.button("Apply Theme Preferences"):
            st.session_state.theme = theme_choice
            st.success(f"Theme set to {theme_choice}!")
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="glass-card" style="border-color: rgba(239, 68, 68, 0.3);">
                <h4 style="color:#F87171; margin-top:0;">🗄️ Database & Storage Management</h4>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat Session History"):
            try:
                clear_chat_history(user_id=user_id)
                st.success("Chat history cleared from SQLite database!")
            except Exception as e:
                st.error(f"Error: {e}")
            st.rerun()
            
        if st.button("🔄 Reset Local Database Tables"):
            try:
                init_db()
                st.success("SQLite database initialized successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    
    # DEVELOPER CREDITS & ABOUT PROJECT SECTION
    st.markdown("""
        <div class="glass-card" style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(56, 189, 248, 0.3);">
            <h3 style="color:#38BDF8; margin-top:0;">📌 About Project & Developer Credits</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
                <div>
                    <p style="color:#CBD5E1; font-size:0.95rem; margin-bottom:8px;">• <strong>Project Name:</strong> <span style="color:#F8FAFC; font-weight:700;">CareerMate-AI</span></p>
                    <p style="color:#CBD5E1; font-size:0.95rem; margin-bottom:8px;">• <strong>Developed by:</strong> <span style="color:#38BDF8; font-weight:800; font-size:1.05rem;">Upputuri Srilakshmihari</span></p>
                    <p style="color:#CBD5E1; font-size:0.95rem; margin-bottom:8px;">• <strong>Purpose:</strong> AI-powered career guidance and internship recommendation system for college students.</p>
                </div>
                <div>
                    <p style="color:#CBD5E1; font-size:0.95rem; margin-bottom:8px;">• <strong>Core Technologies:</strong> Python 3.11+, Streamlit, Scikit-learn (TF-IDF & Cosine Similarity), SQLite3, PyPDF, Web Speech API.</p>
                    <p style="color:#CBD5E1; font-size:0.95rem; margin-bottom:8px;">• <strong>Version:</strong> 2.0.0 (Production Release)</p>
                    <p style="color:#CBD5E1; font-size:0.95rem; margin-bottom:0;">• <strong>Architecture:</strong> 100% Offline Capable & Zero Paid API Dependency.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_settings_page()

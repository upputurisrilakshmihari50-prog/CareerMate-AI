from pathlib import Path
import streamlit as st
import sys

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from utils import load_css, init_session_state
from database import init_db, get_or_create_default_user

# Import page modules
from pages.auth import render_auth_page
from pages.dashboard import render_dashboard_page
from pages.chat import render_chat_page
from pages.careers import render_careers_page
from pages.internships import render_internships_page
from pages.skills import render_skills_page
from pages.roadmap import render_roadmap_page
from pages.interview import render_interview_page
from pages.resume import render_resume_page
from pages.profile import render_profile_page
from pages.settings import render_settings_page

# Page Configuration
st.set_page_config(
    page_title="CareerMate-AI 🚀 | Developed by Upputuri Srilakshmihari",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database & Session State
init_db()
init_session_state()
load_css()

# UNAUTHENTICATED USER ROUTING GATING:
# If user is not authenticated, FORCE active page to "Login / Register"
if not st.session_state.get("is_authenticated", False):
    st.session_state.active_page = "Login / Register"

# SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 12px 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 16px;">
            <h1 style="font-size: 1.6rem; margin: 0; background: linear-gradient(90deg, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">
                CareerMate-AI 🚀
            </h1>
            <p style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px; font-weight: 500;">
                AI-Powered Career Guidance
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # If user is authenticated, show full navigation menu
    if st.session_state.get("is_authenticated", False):
        if st.button("✨ + New Chat", use_container_width=True):
            st.session_state.active_page = "AI Career Chat"
            st.rerun()
            
        st.write("")
        st.markdown("<span style='color: #64748B; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;'>NAVIGATION MENU</span>", unsafe_allow_html=True)
        
        nav_options = [
            "Dashboard",
            "AI Career Chat",
            "Career Recommendations",
            "Internship Finder",
            "Skill Gap Analysis",
            "Learning Roadmap",
            "Interview Preparation",
            "Resume Analyzer",
            "My Profile",
            "Settings"
        ]
        
        nav_icons = {
            "Dashboard": "📊",
            "AI Career Chat": "🤖",
            "Career Recommendations": "🚀",
            "Internship Finder": "💼",
            "Skill Gap Analysis": "🎯",
            "Learning Roadmap": "🗺️",
            "Interview Preparation": "🎙️",
            "Resume Analyzer": "📄",
            "My Profile": "👤",
            "Settings": "⚙️"
        }
        
        current_page = st.session_state.get("active_page", "Dashboard")
        current_index = nav_options.index(current_page) if current_page in nav_options else 0
        
        selected_nav = st.radio(
            "Navigate",
            options=nav_options,
            format_func=lambda x: f"{nav_icons[x]} {x}",
            index=current_index,
            label_visibility="collapsed"
        )
        
        if selected_nav != st.session_state.active_page:
            st.session_state.active_page = selected_nav
            st.rerun()
            
        st.write("---")
        
        user_info = st.session_state.get("user", {}) or {}
        user_name = user_info.get("name", st.session_state.get("username", "Student User"))
        user_branch = user_info.get("branch", "B.Tech CSE")
        
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.7); padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.4rem;">🎓</span>
                    <div>
                        <div style="font-weight: 700; color: #F8FAFC; font-size: 0.85rem;">{user_name}</div>
                        <div style="color: #94A3B8; font-size: 0.75rem;">{user_branch}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            if st.button("🌙 Dark", use_container_width=True):
                st.session_state.theme = "Dark Navy"
                st.rerun()
        with col_t2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.is_authenticated = False
                st.session_state.user = None
                st.session_state.active_page = "Login / Register"
                st.rerun()
    else:
        st.info("🔐 Please log in to unlock full navigation.")
        if st.button("🔐 Sign In / Register", use_container_width=True, type="primary"):
            st.session_state.active_page = "Login / Register"
            st.rerun()

    st.write("---")
    st.markdown("""
        <div style="text-align: center; font-size: 0.78rem; color: #94A3B8; padding-top: 4px;">
            <div><strong>CareerMate-AI</strong></div>
            <div>Developed by <strong style="color:#38BDF8;">Upputuri Srilakshmihari</strong></div>
        </div>
    """, unsafe_allow_html=True)

# PAGE ROUTING LOGIC WITH AUTHENTICATION PROTECTION
active_page = st.session_state.get("active_page", "Login / Register")

if not st.session_state.get("is_authenticated", False):
    render_auth_page()
else:
    if active_page == "Login / Register":
        render_auth_page()
    elif active_page == "Dashboard":
        render_dashboard_page()
    elif active_page == "AI Career Chat":
        render_chat_page()
    elif active_page == "Career Recommendations":
        render_careers_page()
    elif active_page == "Internship Finder":
        render_internships_page()
    elif active_page == "Skill Gap Analysis":
        render_skills_page()
    elif active_page == "Learning Roadmap":
        render_roadmap_page()
    elif active_page == "Interview Preparation":
        render_interview_page()
    elif active_page == "Resume Analyzer":
        render_resume_page()
    elif active_page == "My Profile":
        render_profile_page()
    elif active_page == "Settings":
        render_settings_page()
    else:
        render_dashboard_page()

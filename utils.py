from pathlib import Path
import streamlit as st
from database import get_user_skills, get_quiz_stats, get_saved_recommendations

BASE_DIR = Path(__file__).resolve().parent
CSS_PATH = BASE_DIR / "assets" / "style.css"

def load_css():
    if CSS_PATH.exists():
        try:
            with open(CSS_PATH, "r", encoding="utf-8") as f:
                css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        except Exception as e:
            print(f"[load_css Error] {e}")

def init_session_state():
    """
    Safely initialize all required Streamlit session state variables.
    Default unauthenticated user lands on Login page.
    """
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
        
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = st.session_state.is_authenticated
        
    if "user" not in st.session_state:
        st.session_state.user = None
        
    user_dict = st.session_state.get("user", {}) or {}
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = user_dict.get("id", 1) if user_dict else 1
        
    if "username" not in st.session_state:
        st.session_state.username = user_dict.get("name", "Student User") if user_dict else "Guest"
        
    if "skills" not in st.session_state or not st.session_state.skills:
        u_skills = get_user_skills(st.session_state.user_id)
        st.session_state.skills = u_skills if u_skills else ['Python', 'SQL', 'Git']
        
    if "user_skills" not in st.session_state or not st.session_state.user_skills:
        st.session_state.user_skills = st.session_state.skills
        
    if "interests" not in st.session_state:
        st.session_state.interests = user_dict.get("interests", "Artificial Intelligence, Web Development") if user_dict else "Artificial Intelligence"
        
    if "profile" not in st.session_state:
        st.session_state.profile = user_dict
        
    if "career_recommendations" not in st.session_state:
        st.session_state.career_recommendations = []
        
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Login / Register" if not st.session_state.is_authenticated else "Dashboard"
        
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark Navy"
        
    if "selected_career" not in st.session_state:
        st.session_state.selected_career = "Python Developer"

def render_header(title, tagline):
    st.markdown(f"""
        <div class="header-banner">
            <h1>{title}</h1>
            <p style="color: #94A3B8; font-size: 1.1rem; margin-top: 8px; font-weight: 500;">{tagline}</p>
        </div>
    """, unsafe_allow_html=True)

def get_dashboard_metrics(user_id=1):
    try:
        skills = get_user_skills(user_id)
        recs = get_saved_recommendations(user_id)
        q_stats = get_quiz_stats(user_id)
        
        return {
            "skills_count": len(skills) if skills else 3,
            "careers_matched": len(recs) if recs else 12,
            "internships_recommended": 8,
            "quiz_practiced": q_stats['total_qs'] if q_stats else 0
        }
    except Exception as e:
        print(f"[get_dashboard_metrics Error] {e}")
        return {
            "skills_count": 3,
            "careers_matched": 12,
            "internships_recommended": 8,
            "quiz_practiced": 0
        }

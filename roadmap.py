import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from recommendation import generate_learning_roadmap
from database import init_db
from utils import load_css, init_session_state

def render_roadmap_page():
    init_db()
    init_session_state()
    load_css()
    
    selected_career = st.session_state.get("selected_career", "Python Developer")
    
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC;">🗺️ Learning Roadmap</h2>
            <p style="color: #94A3B8;">Follow this structured timeline to master your target tech role step-by-step.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, _ = st.columns([2, 1])
    with col1:
        career_list = ["Python Developer", "Data Scientist", "Machine Learning Engineer", "Data Analyst", "AI Engineer", "Web Developer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Java Developer", "Android Developer", "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "Database Administrator", "UI UX Designer"]
        sel_idx = career_list.index(selected_career) if selected_career in career_list else 0
        target_role = st.selectbox(
            "Target Role Roadmap:",
            career_list,
            index=sel_idx
        )
        
    try:
        roadmap = generate_learning_roadmap(target_role)
    except Exception as e:
        print(f"[Roadmap Warning] {e}")
        roadmap = {"Career": target_role, "Steps": []}
    
    st.write("")
    st.markdown(f"<h3 style='color: #38BDF8;'>{roadmap['Career']} Preparation Timeline</h3>", unsafe_allow_html=True)
    
    # Render timeline steps
    for step in roadmap['Steps']:
        st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #38BDF8; position: relative;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="background: rgba(56, 189, 248, 0.2); color: #38BDF8; font-weight: 800; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem;">
                        STEP {step['Step_Number']}
                    </span>
                    <span style="color: #818CF8; font-weight: 600; font-size: 0.85rem;">⏱️ {step['Duration']}</span>
                </div>
                <h3 style="margin: 4px 0 8px 0; color: #F8FAFC; font-size: 1.2rem;">{step['Title']}</h3>
                <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">{step['Description']}</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_roadmap_page()

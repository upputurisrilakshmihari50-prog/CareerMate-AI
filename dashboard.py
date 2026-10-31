import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from recommendation import get_career_recommendations
from utils import get_dashboard_metrics, load_css, init_session_state
from database import init_db

def render_dashboard_page():
    init_db()
    init_session_state()
    load_css()
    
    user = st.session_state.get("user", {}) or {}
    user_name = user.get("name", st.session_state.get("username", "Student"))
    user_skills_list = st.session_state.get("user_skills") or st.session_state.get("skills") or ["Python", "SQL", "Git"]
    skills_str = ", ".join(user_skills_list)
    
    # Welcome banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9)); border: 1px solid rgba(56,189,248,0.2); border-radius: 16px; padding: 28px; margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC; font-weight: 800; font-size: 1.8rem;">Welcome to CareerMate AI 👋, {user_name}!</h2>
            <p style="color: #38BDF8; font-size: 1.1rem; margin-top: 6px; font-weight: 600;">Discover tech careers and internship opportunities perfectly matched to your skills.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Statistics Cards
    metrics = get_dashboard_metrics(user.get("id", st.session_state.get("user_id", 1)))
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{metrics['skills_count']}</div>
                <div class="stat-label">Skills Added</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{metrics['careers_matched']}</div>
                <div class="stat-label">Careers Matched</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{metrics['internships_recommended']}</div>
                <div class="stat-label">Internships Available</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{metrics['quiz_practiced']}</div>
                <div class="stat-label">Questions Practiced</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # Recommended Careers Section
    st.markdown("<h3 style='color: #F8FAFC; font-weight: 700;'>🌟 Top Recommended Careers For You</h3>", unsafe_allow_html=True)
    st.caption("Powered by TF-IDF Vectorization & Cosine Similarity ML Engine")
    
    try:
        recs = get_career_recommendations(skills_str=skills_str, top_n=8)
    except Exception as e:
        from model import get_rule_based_fallback_recommendations
        recs = get_rule_based_fallback_recommendations(skills_str, top_n=8)
        
    # Render cards in 2-column grid
    for i in range(0, len(recs), 2):
        c1, c2 = st.columns(2)
        
        for idx, col in enumerate([c1, c2]):
            if i + idx < len(recs):
                item = recs[i + idx]
                with col:
                    skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in item['Required_Skills'][:4]])
                    tools_html = "".join([f'<span style="display:inline-block; background:rgba(255,255,255,0.06); color:#E2E8F0; padding:2px 8px; border-radius:12px; font-size:0.75rem; margin-right:4px;">{t}</span>' for t in item['Tools'][:3]])
                    
                    st.markdown(f"""
                        <div class="glass-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <h4 style="margin: 0; color: #F8FAFC; font-size: 1.25rem;">{item['Role']}</h4>
                                <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">{item['Match_Percentage']}% Match</span>
                            </div>
                            <p style="color: #94A3B8; font-size: 0.9rem; min-height: 48px;">{item['Description']}</p>
                            <div style="margin-bottom: 10px;">
                                <strong style="color: #CBD5E1; font-size: 0.8rem; display: block; margin-bottom: 4px;">REQUIRED SKILLS:</strong>
                                {skills_html}
                            </div>
                            <div style="margin-bottom: 16px;">
                                <strong style="color: #CBD5E1; font-size: 0.8rem; display: block; margin-bottom: 4px;">TOOLS:</strong>
                                {tools_html}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View Details & Roadmap", key=f"btn_dash_{item['Role'].replace(' ', '_')}_{i+idx}"):
                        st.session_state.selected_career = item['Role']
                        st.session_state.active_page = "Learning Roadmap"
                        st.rerun()

if __name__ == "__main__":
    render_dashboard_page()

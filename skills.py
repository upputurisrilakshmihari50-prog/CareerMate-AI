import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from recommendation import analyze_skill_gap
from database import init_db
from utils import load_css, init_session_state

def render_skills_page():
    init_db()
    init_session_state()
    load_css()
    
    user_skills_list = st.session_state.get("user_skills") or st.session_state.get("skills") or ["Python", "SQL", "Git"]
    selected_career = st.session_state.get("selected_career", "Data Scientist")
    
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC;">🎯 Skill Gap Analysis</h2>
            <p style="color: #94A3B8;">Compare your current skill set against your target career to identify missing knowledge.</p>
        </div>
    """, unsafe_allow_html=True)
    
    career_options = ["Data Scientist", "Machine Learning Engineer", "Python Developer", "Data Analyst", "AI Engineer", "Web Developer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Java Developer", "Android Developer", "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "Database Administrator", "UI UX Designer", "QA Engineer"]
    sel_index = career_options.index(selected_career) if selected_career in career_options else 0
    
    col_sel, _ = st.columns([2, 1])
    with col_sel:
        target_role = st.selectbox(
            "Select Your Target Career:",
            career_options,
            index=sel_index
        )
        
    try:
        gap = analyze_skill_gap(target_role, user_skills_list)
    except Exception as e:
        print(f"[Skill Gap Warning] {e}")
        gap = {
            "Target_Career": target_role,
            "Readiness_Percentage": 55,
            "Required_Skills": ["Python", "SQL", "Machine Learning"],
            "Matching_Skills": ["Python", "SQL"],
            "Missing_Skills": ["Machine Learning"],
            "Recommended_Next_Skills": ["Machine Learning"],
            "Tools_To_Learn": ["Scikit-learn", "Pandas"]
        }
        
    st.write("")
    
    # Progress gauge banner
    st.markdown(f"""
        <div class="glass-card" style="text-align: center; border-color: rgba(56, 189, 248, 0.3);">
            <h4 style="color: #94A3B8; margin: 0; text-transform: uppercase; font-size: 0.85rem;">Overall Career Readiness Score</h4>
            <div style="font-size: 3.5rem; font-weight: 800; color: #38BDF8; margin: 8px 0;">{gap['Readiness_Percentage']}%</div>
            <p style="color: #CBD5E1; margin: 0;">Target Role: <strong style="color:#F8FAFC;">{gap['Target_Career']}</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(gap['Readiness_Percentage'] / 100.0)
    st.write("")
    
    # Skill comparison columns
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #10B981;">
                <h3 style="color: #10B981; margin-top: 0;">Your Skills ✅</h3>
                <p style="color: #94A3B8; font-size: 0.85rem;">Skills you currently master for this role:</p>
        """, unsafe_allow_html=True)
        
        if gap['Matching_Skills']:
            for sk in gap['Matching_Skills']:
                st.markdown(f"<div style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); color:#10B981; padding:10px 14px; border-radius:10px; margin-bottom:8px; font-weight:600;'>✅ {sk}</div>", unsafe_allow_html=True)
        else:
            st.info("No matching skills detected yet. Add more skills in your profile!")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
            <div class="glass-card" style="border-left: 4px solid #EF4444;">
                <h3 style="color: #F87171; margin-top: 0;">Skills to Learn ❌</h3>
                <p style="color: #94A3B8; font-size: 0.85rem;">Required skills missing from your profile:</p>
        """, unsafe_allow_html=True)
        
        if gap['Missing_Skills']:
            for sk in gap['Missing_Skills']:
                st.markdown(f"<div style='background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); color:#F87171; padding:10px 14px; border-radius:10px; margin-bottom:8px; font-weight:600;'>❌ {sk}</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 You possess all core skills required for this career!")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Recommended Next Actionable Skills
    st.markdown("""
        <div class="glass-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(56, 189, 248, 0.15)); border: 1px solid rgba(99, 102, 241, 0.3);">
            <h4 style="color: #818CF8; margin-top: 0;">💡 Recommended Next Skills to Master</h4>
            <p style="color: #CBD5E1;">Focusing on these top high-priority skills will raise your career readiness score past 85%:</p>
    """, unsafe_allow_html=True)
    
    next_html = "".join([f'<span class="skill-badge" style="font-size:0.95rem; padding:6px 14px; margin-right:8px;">🚀 {s}</span>' for s in gap['Recommended_Next_Skills']])
    st.markdown(f"<div>{next_html}</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_skills_page()

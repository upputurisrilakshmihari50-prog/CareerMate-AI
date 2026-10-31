import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from recommendation import get_career_recommendations
from database import save_recommendation, init_db
from utils import load_css, init_session_state

def render_careers_page():
    init_db()
    init_session_state()
    load_css()
    
    user = st.session_state.get("user", {}) or {}
    user_skills_list = st.session_state.get("user_skills") or st.session_state.get("skills") or ["Python", "SQL", "Machine Learning"]
    
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC;">🚀 Career Recommendations</h2>
            <p style="color: #94A3B8;">Enter your technical skills and background to generate ML-based career suggestions and job roles.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input Form Card
    with st.form("career_recommendation_form"):
        st.markdown("<h4 style='color: #38BDF8;'>📋 Your Career Profile Inputs</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            skills_input = st.text_area("Your Skills (comma separated)", value=", ".join(user_skills_list), help="Example: Python, SQL, Machine Learning, Git")
            education_input = st.selectbox("Education Level", ["B.Tech CSE / IT", "B.Sc Computer Science / Stats", "BCA / MCA", "M.Tech Data Science", "Other Engineering"])
            interests_input = st.text_input("Interests & Specializations", value=st.session_state.get("interests", "Artificial Intelligence, Web Development"), help="Example: Data Science, Cloud, Web Apps")
            
        with col2:
            field_input = st.selectbox("Preferred Industry Field", ["All", "Software & Web Services", "Analytics & Consulting", "Artificial Intelligence", "Cloud Services", "Cybersecurity", "Mobile Development"])
            experience_input = st.selectbox("Experience Level", ["All", "Entry Level", "Junior", "Intermediate", "Mid-Level"])
            top_n_input = st.slider("Number of Recommendations", min_value=3, max_value=8, value=5)
            
        submit_btn = st.form_submit_button("✨ Find Matching Careers", use_container_width=True)
        
    st.write("")
    
    # Process Recommendation with safe fallback logic
    skills_query = skills_input if skills_input.strip() else ", ".join(user_skills_list)
    
    try:
        recs = get_career_recommendations(
            skills_str=skills_query,
            education=education_input,
            field=field_input,
            experience=experience_input,
            interests=interests_input,
            top_n=top_n_input
        )
    except Exception as e:
        st.warning("Notice: Machine learning engine unavailable, displaying rule-based fallback recommendations.")
        from model import get_rule_based_fallback_recommendations
        recs = get_rule_based_fallback_recommendations(skills_query, top_n=top_n_input)
        
    if not recs:
        from model import get_rule_based_fallback_recommendations
        recs = get_rule_based_fallback_recommendations(skills_query, top_n=top_n_input)

    st.session_state.career_recommendations = recs

    # Save top recommendation to database
    if recs and user.get("id"):
        try:
            save_recommendation(user['id'], recs[0]['Role'], recs[0]['Match_Percentage'])
        except Exception as e:
            print(f"[Save Rec Warning] {e}")
        
    st.markdown(f"<h3 style='color: #F8FAFC;'>Matched Tech Careers ({len(recs)} Found)</h3>", unsafe_allow_html=True)
    
    for idx, item in enumerate(recs, 1):
        matching_html = "".join([f'<span class="skill-badge">{s}</span>' for s in item['Matching_Skills']])
        missing_html = "".join([f'<span class="skill-badge-missing">{s}</span>' for s in item['Missing_Skills']]) if item['Missing_Skills'] else '<span style="color:#10B981; font-weight:600;">None (100% Core Skills Matched)</span>'
        tools_html = "".join([f'<span style="background:rgba(255,255,255,0.08); color:#E2E8F0; padding:2px 10px; border-radius:12px; font-size:0.8rem; margin-right:6px;">{t}</span>' for t in item['Tools']])
        
        st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 16px;">
                    <div>
                        <h3 style="margin: 0; color: #F8FAFC; font-size: 1.4rem;">{idx}. {item['Role']}</h3>
                        <span style="color: #94A3B8; font-size: 0.85rem;">Industry: {item['Industry']} | Salary: {item['Salary_Range']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: linear-gradient(135deg, #10B981, #059669); color: #FFF; padding: 6px 16px; border-radius: 20px; font-weight: 800; font-size: 1rem;">{item['Match_Percentage']}% MATCH</span>
                    </div>
                </div>
                <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 16px;"><strong>Career Description:</strong> {item['Description']}</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                    <div>
                        <strong style="color: #38BDF8; font-size: 0.85rem; display: block; margin-bottom: 6px;">✅ REQUIRED / MATCHING SKILLS:</strong>
                        <div>{matching_html}</div>
                    </div>
                    <div>
                        <strong style="color: #F87171; font-size: 0.85rem; display: block; margin-bottom: 6px;">❌ SKILLS TO LEARN:</strong>
                        <div>{missing_html}</div>
                    </div>
                </div>
                <div style="margin-bottom: 16px;">
                    <strong style="color: #818CF8; font-size: 0.85rem; display: block; margin-bottom: 6px;">🛠️ KEY TOOLS & TECH STACK:</strong>
                    <div>{tools_html}</div>
                </div>
                <div style="background: rgba(15,23,42,0.6); padding: 12px 16px; border-radius: 10px; border-left: 4px solid #38BDF8; margin-bottom: 12px;">
                    <strong style="color: #F8FAFC; font-size: 0.85rem;">🗺️ LEARNING ROADMAP PATHWAY:</strong>
                    <p style="color: #94A3B8; font-size: 0.85rem; margin: 4px 0 0 0;">{item['Learning_Path']}</p>
                </div>
                <div style="background: rgba(15,23,42,0.4); padding: 10px 14px; border-radius: 8px;">
                    <strong style="color: #818CF8; font-size: 0.8rem;">💼 RECOMMENDED JOB ROLE TARGETS:</strong>
                    <span style="color: #CBD5E1; font-size: 0.85rem; margin-left: 6px;">{item.get('Internship', item['Role'] + ' Intern')} & Entry Level {item['Role']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        c_btn, _ = st.columns([2, 5])
        with c_btn:
            if st.button(f"Analyze Skill Gap for {item['Role']}", key=f"btn_gap_{idx}"):
                st.session_state.selected_career = item['Role']
                st.session_state.active_page = "Skill Gap Analysis"
                st.rerun()

# Run immediately when executed directly by Streamlit
if __name__ == "__main__":
    render_careers_page()

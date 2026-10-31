import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from database import update_user_profile, update_user_skills, get_or_create_default_user, get_user_skills, init_db
from utils import load_css, init_session_state

def render_profile_page():
    init_db()
    init_session_state()
    load_css()
    
    user = st.session_state.get("user") or get_or_create_default_user()
    user_id = user.get("id", st.session_state.get("user_id", 1))
    user_skills_list = get_user_skills(user_id)
    
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC;">👤 My Student Profile</h2>
            <p style="color: #94A3B8;">Manage your academic details, technical skills, and career preferences saved in SQLite database.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("profile_edit_form"):
        st.markdown("<h4 style='color:#38BDF8;'>Personal & Academic Details</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            name_val = st.text_input("Full Name", value=user.get("name", st.session_state.get("username", "Student User")))
            degree_options = ["B.Tech CSE", "B.Tech IT", "B.Tech ECE", "B.Sc Computer Science", "BCA", "MCA", "M.Tech AI/DS"]
            curr_edu = user.get("education", "B.Tech CSE")
            edu_index = degree_options.index(curr_edu) if curr_edu in degree_options else 0
            edu_val = st.selectbox("Education Degree", degree_options, index=edu_index)
            branch_val = st.text_input("Department / Branch", value=user.get("branch", "Computer Science & Engineering"))
            
            year_options = ["2024", "2025", "2026", "2027", "2028"]
            curr_year = user.get("graduation_year", "2026")
            year_index = year_options.index(curr_year) if curr_year in year_options else 2
            grad_val = st.selectbox("Graduation Year", year_options, index=year_index)
            
        with col2:
            exp_options = ["Entry Level", "Junior", "Intermediate", "Mid-Level"]
            curr_exp = user.get("experience_level", "Entry Level")
            exp_index = exp_options.index(curr_exp) if curr_exp in exp_options else 0
            exp_val = st.selectbox("Experience Level", exp_options, index=exp_index)
            
            career_options = ["Python Developer", "Data Analyst", "Data Scientist", "Machine Learning Engineer", "Web Developer", "Java Developer", "Full Stack Developer", "Cloud Engineer", "Cybersecurity Analyst"]
            curr_target = user.get("target_career", "Python Developer")
            target_index = career_options.index(curr_target) if curr_target in career_options else 0
            target_val = st.selectbox("Target Career Preference", career_options, index=target_index)
            
            interests_val = st.text_input("Specialized Interests", value=user.get("interests", "Artificial Intelligence, Full Stack Web"))
            
        st.write("---")
        st.markdown("<h4 style='color:#38BDF8;'>My Technical Skills (Comma Separated)</h4>", unsafe_allow_html=True)
        skills_str_val = st.text_area("Current Skills", value=", ".join(user_skills_list), help="Separate each skill with a comma, e.g., Python, SQL, Git, React")
        
        save_btn = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)
        
        if save_btn:
            update_user_profile(
                user_id=user_id,
                name=name_val,
                education=edu_val,
                branch=branch_val,
                graduation_year=grad_val,
                interests=interests_val,
                experience_level=exp_val,
                target_career=target_val
            )
            
            new_skills = [s.strip() for s in skills_str_val.split(",") if s.strip()]
            update_user_skills(user_id, new_skills)
            
            updated_user = get_or_create_default_user()
            updated_user['name'] = name_val
            updated_user['education'] = edu_val
            updated_user['branch'] = branch_val
            updated_user['graduation_year'] = grad_val
            updated_user['interests'] = interests_val
            updated_user['experience_level'] = exp_val
            updated_user['target_career'] = target_val
            
            st.session_state.user = updated_user
            st.session_state.user_skills = new_skills
            st.session_state.skills = new_skills
            st.session_state.interests = interests_val
            st.session_state.username = name_val
            st.session_state.selected_career = target_val
            
            st.success("🎉 Profile and skills successfully saved!")
            st.rerun()

if __name__ == "__main__":
    render_profile_page()

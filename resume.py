import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from resume_analyzer import extract_text_from_pdf, analyze_resume_text
from database import init_db
from utils import load_css, init_session_state

def render_resume_page():
    init_db()
    init_session_state()
    load_css()
    
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC;">📄 AI Resume Analyzer</h2>
            <p style="color: #94A3B8;">Upload your PDF resume to extract skills, evaluate keyword match score, and get instant recommendations.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("📌 **Disclaimer:** Resume scoring is calculated based on keyword density, standard technical section markers, and dataset skill alignments. It provides optimization suggestions and does not guarantee automated hiring decisions.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h4 style='color:#38BDF8;'>Upload PDF Resume</h4>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], help="Supported format: PDF")
        
        target_role = st.selectbox(
            "Select Target Role for Comparison:",
            ["Python Developer", "Data Scientist", "Data Analyst", "Machine Learning Engineer", "Web Developer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Java Developer", "Cloud Engineer", "Cybersecurity Analyst"]
        )
        
    if uploaded_file is not None:
        with st.spinner("Extracting text and running NLP skill match analysis..."):
            text = extract_text_from_pdf(uploaded_file)
            analysis = analyze_resume_text(text, target_career=target_role)
            
        if "error" in analysis:
            st.error(analysis["error"])
        else:
            with col2:
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center; border-color: rgba(56, 189, 248, 0.4);">
                        <h4 style="color: #94A3B8; margin: 0;">OVERALL RESUME MATCH SCORE</h4>
                        <div style="font-size: 3.5rem; font-weight: 800; color: #38BDF8; margin: 6px 0;">{analysis['Resume_Score']} / 100</div>
                        <p style="color: #CBD5E1; margin: 0;">Target Role: <strong style="color:#FFF;">{target_role}</strong></p>
                    </div>
                """, unsafe_allow_html=True)
                
            st.write("---")
            st.markdown("<h3 style='color:#F8FAFC;'>Resume Detailed Feedback</h3>", unsafe_allow_html=True)
            
            c_left, c_right = st.columns(2)
            
            with c_left:
                st.markdown("""
                    <div class="glass-card">
                        <h4 style="color:#10B981; margin-top:0;">Skills Detected in Resume</h4>
                """, unsafe_allow_html=True)
                
                skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in analysis['Detected_Skills']])
                st.markdown(f"<div>{skills_html}</div></div>", unsafe_allow_html=True)
                
                st.markdown("""
                    <div class="glass-card">
                        <h4 style="color:#818CF8; margin-top:0;">Resume Section Checklist</h4>
                """, unsafe_allow_html=True)
                
                for section, found in analysis['Sections_Found'].items():
                    status_icon = "✅" if found else "⚠️ Missing"
                    color_style = "#10B981" if found else "#F59E0B"
                    st.markdown(f"<div style='display:flex; justify-space-between; margin-bottom:6px;'><span>{section}</span><strong style='color:{color_style};'>{status_icon}</strong></div>", unsafe_allow_html=True)
                    
                st.markdown("</div>", unsafe_allow_html=True)
                
            with c_right:
                st.markdown("""
                    <div class="glass-card" style="border-left: 4px solid #F59E0B;">
                        <h4 style="color:#F59E0B; margin-top:0;">Missing Target Keywords</h4>
                        <p style="color:#94A3B8; font-size:0.85rem;">Skills commonly expected for {target_role} missing from your resume:</p>
                """, unsafe_allow_html=True)
                
                missing_html = "".join([f'<span class="skill-badge-missing">{s}</span>' for s in analysis['Missing_Target_Keywords']]) if analysis['Missing_Target_Keywords'] else '<span style="color:#10B981;">No critical skills missing!</span>'
                st.markdown(f"<div>{missing_html}</div></div>", unsafe_allow_html=True)
                
                st.markdown("""
                    <div class="glass-card" style="border-left: 4px solid #38BDF8;">
                        <h4 style="color:#38BDF8; margin-top:0;">💡 Recommended Improvement Tips</h4>
                """, unsafe_allow_html=True)
                
                for sug in analysis['Suggestions']:
                    st.markdown(f"• {sug}")
                    
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        with col2:
            st.markdown("""
                <div class="glass-card" style="text-align: center; padding: 40px 20px;">
                    <span style="font-size: 3rem;">📄</span>
                    <h3 style="color: #F8FAFC; margin-top: 10px;">Upload PDF to Analyze</h3>
                    <p style="color: #94A3B8;">Select your resume file on the left to view skill detection, keyword alignment, and formatting suggestions.</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_resume_page()

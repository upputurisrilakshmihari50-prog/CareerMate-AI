import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from interview import filter_questions, get_quiz_questions
from database import save_quiz_score, get_quiz_stats, init_db
from utils import load_css, init_session_state

def render_interview_page():
    init_db()
    init_session_state()
    load_css()
    
    user = st.session_state.get("user", {}) or {}
    user_id = user.get("id", st.session_state.get("user_id", 1))
    
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="margin: 0; color: #F8FAFC;">🎙️ Interview Preparation & Practice</h2>
            <p style="color: #94A3B8;">Master technical, coding, SQL, and HR interview questions for top tech roles.</p>
        </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["📚 Question Bank Explorer", "🧠 Interactive Quiz Mode", "📊 Quiz History & Performance"])
    
    # TAB 1: QUESTION BANK EXPLORER
    with tabs[0]:
        col1, col2, col3 = st.columns(3)
        with col1:
            career_filter = st.selectbox("Filter Career Role:", ["All", "Python Developer", "Data Analyst", "Data Scientist", "Machine Learning Engineer", "Java Developer", "Full Stack Developer", "Cloud Engineer", "Cybersecurity Analyst"])
        with col2:
            cat_filter = st.selectbox("Category:", ["All", "Technical", "HR", "Coding", "SQL", "Python", "Java", "Machine Learning", "Web Development"])
        with col3:
            diff_filter = st.selectbox("Difficulty Level:", ["All", "Easy", "Medium", "Hard"])
            
        questions = filter_questions(career=career_filter, category=cat_filter, difficulty=diff_filter)
        
        st.write("")
        st.markdown(f"<h4 style='color:#38BDF8;'>Showing {len(questions)} Questions</h4>", unsafe_allow_html=True)
        
        for q in questions[:15]:
            diff_color = "#10B981" if q['Difficulty'] == "Easy" else "#F59E0B" if q['Difficulty'] == "Medium" else "#EF4444"
            with st.expander(f"❓ {q['Question']} ({q['Category']} | {q['Difficulty']})"):
                st.markdown(f"**Answer:**\n{q['Answer']}")
                st.markdown(f"**Explanation:**\n_{q['Explanation']}_")
                st.markdown(f"<span style='color:{diff_color}; font-weight:700; font-size:0.8rem;'>Difficulty: {q['Difficulty']}</span>", unsafe_allow_html=True)

    # TAB 2: INTERACTIVE QUIZ MODE
    with tabs[1]:
        st.markdown("<h3 style='color:#F8FAFC;'>Test Your Skill Readiness</h3>", unsafe_allow_html=True)
        
        if "quiz_active" not in st.session_state:
            st.session_state.quiz_active = False
            st.session_state.quiz_data = []
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            
        if not st.session_state.quiz_active:
            q_category = st.selectbox("Select Quiz Topic:", ["Python", "SQL", "Machine Learning", "Java", "Web Development", "Technical", "HR"])
            if st.button("🚀 Start 5-Question Quiz", type="primary"):
                st.session_state.quiz_data = get_quiz_questions(category=q_category, count=5)
                st.session_state.quiz_topic = q_category
                st.session_state.quiz_active = True
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {}
                st.rerun()
        else:
            st.markdown(f"#### Topic: `{st.session_state.quiz_topic}`")
            
            with st.form("quiz_form"):
                for idx, item in enumerate(st.session_state.quiz_data, 1):
                    st.markdown(f"**Q{idx}. {item['Question']}**")
                    selected_opt = st.radio(
                        f"Select your answer for Q{idx}:",
                        item['Options'],
                        key=f"q_radio_{idx}"
                    )
                    st.session_state.quiz_answers[idx] = selected_opt
                    st.write("---")
                    
                submit_quiz = st.form_submit_button("Submit Quiz Answers")
                
            if submit_quiz:
                score = 0
                total = len(st.session_state.quiz_data)
                
                st.markdown("### 📝 Quiz Results")
                for idx, item in enumerate(st.session_state.quiz_data, 1):
                    user_ans = st.session_state.quiz_answers.get(idx)
                    correct_ans = item['Correct_Answer']
                    if user_ans == correct_ans:
                        score += 1
                        st.success(f"**Q{idx}: Correct!** ✅\nAnswer: {correct_ans}\n_{item['Explanation']}_")
                    else:
                        st.error(f"**Q{idx}: Incorrect** ❌\nYour answer: {user_ans}\nCorrect answer: {correct_ans}\n_{item['Explanation']}_")
                        
                score_pct = round((score / total) * 100, 1) if total > 0 else 0
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center; border-color: rgba(16, 185, 129, 0.4);">
                        <h2 style="color: #10B981; margin: 0;">Quiz Completed!</h2>
                        <h1 style="font-size: 3rem; color: #38BDF8; margin: 10px 0;">{score} / {total} ({score_pct}%)</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                try:
                    save_quiz_score(user_id=user_id, topic=st.session_state.quiz_topic, score=score, total_questions=total)
                except Exception as e:
                    print(f"[Quiz Save Warning] {e}")
                
                if st.button("Take Another Quiz"):
                    st.session_state.quiz_active = False
                    st.rerun()

    # TAB 3: QUIZ HISTORY & PERFORMANCE
    with tabs[2]:
        stats = get_quiz_stats(user_id=user_id)
        st.markdown(f"""
            <div class="glass-card">
                <h3>Overall Performance Summary</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; text-align: center; margin-top: 16px;">
                    <div>
                        <div class="stat-number">{stats['attempts']}</div>
                        <div class="stat-label">Total Quizzes</div>
                    </div>
                    <div>
                        <div class="stat-number">{stats['score']} / {stats['total_qs']}</div>
                        <div class="stat-label">Correct Answers</div>
                    </div>
                    <div>
                        <div class="stat-number">{stats['accuracy']}%</div>
                        <div class="stat-label">Overall Accuracy</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_interview_page()

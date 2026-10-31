import streamlit as st
import sys
import re
import html
from pathlib import Path

def get_project_credit_response(user_message: str):
    """Return the project developer's name for implementation questions."""
    message = user_message.lower().strip()

    implementation_phrases = [
        "who implemented",
        "who developed",
        "who created",
        "who made",
        "who is the developer",
        "who is the creator",
        "implemented by whom",
        "project developer",
    ]

    if any(phrase in message for phrase in implementation_phrases):
        return (
            "CareerMate-AI was developed by **Upputuri Srilakshmihari**. "
            "AI tools may also have been used to assist with development "
            "and debugging."
        )

    return None


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from chatbot import process_chat_message
from database import get_chat_history, clear_chat_history, init_db
from utils import load_css, init_session_state

def clean_text_for_speech(text):
    """Strips markdown formatting for clean audio reading."""
    if not text:
        return ""
    text = re.sub(r'#+\s*', '', text)  # remove headings
    text = re.sub(r'\*+([^*]+)\*+', r'\1', text)  # remove bold/italic
    text = re.sub(r'`+([^`]+)`+', r'\1', text)  # remove code formatting
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # remove links
    text = re.sub(r'[•\-\*]\s*', '', text)  # remove bullet points
    text = re.sub(r'\n+', '. ', text)  # convert newlines to pauses
    return text.strip()

def render_chat_page():
    init_db()
    init_session_state()
    load_css()
    
    user = st.session_state.get("user", {}) or {}
    user_id = user.get("id", st.session_state.get("user_id", 1))
    user_skills_list = st.session_state.get("user_skills") or st.session_state.get("skills") or ["Python", "SQL"]
    user_skills_str = ", ".join(user_skills_list)
    
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div>
                <h2 style="margin:0; color:#F8FAFC;">🤖 AI Career Chat (Voice Enabled 🎙️🔊)</h2>
                <p style="color:#94A3B8; margin-top:4px;">Ask CareerMate AI via voice or typing! Supports Speech-to-Text & Text-to-Voice.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Language Preference Bar
    col_lang, _ = st.columns([2, 2])
    with col_lang:
        speech_lang = st.selectbox(
            "🌐 Voice & Speech Language:",
            ["English (US) [en-US]", "English (India) [en-IN]", "Telugu (తెలుగు) [te-IN]"],
            index=0
        )
        lang_code = "en-US" if "en-US" in speech_lang else "en-IN" if "en-IN" in speech_lang else "te-IN"

    # Suggested Prompts Pills
    st.markdown("<strong style='color:#CBD5E1; font-size:0.85rem;'>SUGGESTED QUESTIONS:</strong>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    prompt_to_send = None
    
    with col1:
        if st.button("💡 Career for Python & SQL?"):
            prompt_to_send = "I know Python and SQL. Which career is suitable for me?"
    with col2:
        if st.button("💼 Internships for Java?"):
            prompt_to_send = "I know Java. What internships should I apply for?"
    with col3:
        if st.button("🎯 Skills for Data Analyst?"):
            prompt_to_send = "What skills should I learn to become a Data Analyst?"
    with col4:
        if st.button("🗺️ Python Dev Roadmap?"):
            prompt_to_send = "Give me a roadmap for becoming a Python Developer."
            
    st.write("")
    
    # Load Chat History from SQLite
    history = get_chat_history(user_id=user_id, limit=40)
    
    # Render Chat History Container
    chat_container = st.container()
    
    with chat_container:
        if not history:
            st.markdown("""
                <div class="glass-card" style="text-align: center; padding: 40px 20px;">
                    <span style="font-size: 3rem;">💬</span>
                    <h3 style="color: #F8FAFC; margin-top: 10px;">Start a Conversation</h3>
                    <p style="color: #94A3B8;">Type a question below, click a suggested pill, or use the microphone button to speak!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for idx, item in enumerate(history):
                role = item['role']
                msg = item['message']
                if role == "user":
                    st.markdown(f"""
                        <div class="chat-bubble-user">
                            <div style="font-weight: 700; font-size: 0.8rem; color: #38BDF8; margin-bottom: 4px;">👤 User</div>
                            {msg}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Assistant Bubble with Text-to-Speech (TTS) Speaker Button
                    clean_audio_text = html.escape(clean_text_for_speech(msg))
                    msg_id = f"tts_msg_{idx}"
                    
                    st.markdown(f"""
                        <div class="chat-bubble-ai">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                                <div style="font-weight: 700; font-size: 0.8rem; color: #818CF8;">🤖 CareerMate AI</div>
                                <div>
                                    <button onclick="speakText('{msg_id}', '{lang_code}')" style="background: rgba(56,189,248,0.2); color: #38BDF8; border: 1px solid rgba(56,189,248,0.4); border-radius: 12px; padding: 3px 10px; font-size: 0.78rem; cursor: pointer; font-weight:600;">
                                        🔊 Listen Response
                                    </button>
                                    <button onclick="stopText()" style="background: rgba(239,68,68,0.2); color: #F87171; border: 1px solid rgba(239,68,68,0.4); border-radius: 12px; padding: 3px 10px; font-size: 0.78rem; cursor: pointer; font-weight:600; margin-left: 4px;">
                                        ⏹️ Stop Audio
                                    </button>
                                </div>
                            </div>
                            <div>{msg}</div>
                            <div id="{msg_id}" style="display:none;">{clean_audio_text}</div>
                        </div>
                    """, unsafe_allow_html=True)

    # JavaScript helper script for Web Speech Synthesis & Recognition
    st.components.v1.html(f"""
        <script>
        function speakText(elementId, langCode) {{
            if (!('speechSynthesis' in window)) {{
                alert('Web Speech Synthesis is not supported in this browser.');
                return;
            }}
            window.speechSynthesis.cancel(); // stop previous speech
            
            const textElement = parent.document.getElementById(elementId);
            if (!textElement) return;
            const textToRead = textElement.innerText || textElement.textContent;
            
            if (!textToRead.trim()) return;
            
            const utterance = new SpeechSynthesisUtterance(textToRead);
            utterance.lang = langCode;
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            
            window.speechSynthesis.speak(utterance);
        }}
        
        function stopText() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
            }}
        }}
        </script>
    """, height=0)

    st.write("")
    
    # 🎙️ VOICE & TEXT INPUT CONTROLLER CARD
    st.markdown("""
        <div class="glass-card" style="border: 1px solid rgba(56,189,248,0.3); padding: 18px;">
            <h4 style="color:#38BDF8; margin-top:0; margin-bottom:8px;">🎙️ Voice-to-Text Input (Speech Recognition)</h4>
            <p style="color:#94A3B8; font-size:0.85rem; margin-bottom:12px;">Click the microphone button to dictate your question. You can review and edit the text before sending.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Web Speech Recognition HTML/JS Component
    voice_component = st.components.v1.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: transparent;
                    color: #F8FAFC;
                    margin: 0;
                    padding: 0;
                }}
                .mic-container {{
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    background: rgba(15, 23, 42, 0.8);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    padding: 12px;
                }}
                .mic-btn {{
                    background: linear-gradient(135deg, #0EA5E9, #0284C7);
                    color: white;
                    border: none;
                    border-radius: 50px;
                    padding: 10px 18px;
                    font-size: 0.9rem;
                    font-weight: 700;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    transition: all 0.2s ease;
                }}
                .mic-btn.listening {{
                    background: linear-gradient(135deg, #EF4444, #DC2626);
                    animation: pulse 1.2s infinite;
                }}
                @keyframes pulse {{
                    0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
                    70% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
                    100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
                }}
                .transcript-box {{
                    flex-grow: 1;
                    background: rgba(30, 41, 59, 0.9);
                    border: 1px solid rgba(56, 189, 248, 0.3);
                    border-radius: 8px;
                    color: #F8FAFC;
                    padding: 10px;
                    font-size: 0.95rem;
                    outline: none;
                }}
                .status-msg {{
                    font-size: 0.78rem;
                    color: #94A3B8;
                    margin-top: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="mic-container">
                <button id="micBtn" class="mic-btn" onclick="toggleRecognition()">
                    <span id="micIcon">🎙️</span> <span id="micText">Speak Now</span>
                </button>
                <input type="text" id="transcriptInput" class="transcript-box" placeholder="Dictated text will appear here. Edit anytime..." />
            </div>
            <div id="statusMsg" class="status-msg">Language: {lang_code} | Click 'Speak Now' to start listening.</div>

            <script>
                let recognition = null;
                let isListening = false;
                const lang = '{lang_code}';

                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

                if (!SpeechRecognition) {{
                    document.getElementById('statusMsg').innerHTML = "<span style='color:#F87171;'>⚠️ Speech Recognition is not supported in this browser. Please type below.</span>";
                    document.getElementById('micBtn').disabled = true;
                }} else {{
                    recognition = new SpeechRecognition();
                    recognition.continuous = false;
                    recognition.interimResults = true;
                    recognition.lang = lang;

                    recognition.onstart = function() {{
                        isListening = true;
                        document.getElementById('micBtn').classList.add('listening');
                        document.getElementById('micText').innerText = "Listening...";
                        document.getElementById('statusMsg').innerHTML = "<span style='color:#38BDF8;'>🎤 Listening to your microphone... Speak clearly.</span>";
                    }};

                    recognition.onresult = function(event) {{
                        let currentTranscript = '';
                        for (let i = event.resultIndex; i < event.results.length; i++) {{
                            currentTranscript += event.results[i][0].transcript;
                        }}
                        document.getElementById('transcriptInput').value = currentTranscript;
                    }};

                    recognition.onerror = function(event) {{
                        isListening = false;
                        document.getElementById('micBtn').classList.remove('listening');
                        document.getElementById('micText').innerText = "Speak Now";
                        if (event.error === 'not-allowed') {{
                            document.getElementById('statusMsg').innerHTML = "<span style='color:#F87171;'>⚠️ Microphone permission denied by browser. Please allow mic access.</span>";
                        }} else if (event.error === 'no-speech') {{
                            document.getElementById('statusMsg').innerHTML = "<span style='color:#F59E0B;'>⚠️ No speech detected. Please try speaking again.</span>";
                        }} else {{
                            document.getElementById('statusMsg').innerHTML = "<span style='color:#F87171;'>⚠️ Error: " + event.error + "</span>";
                        }}
                    }};

                    recognition.onend = function() {{
                        isListening = false;
                        document.getElementById('micBtn').classList.remove('listening');
                        document.getElementById('micText').innerText = "Speak Now";
                        const finalVal = document.getElementById('transcriptInput').value;
                        if (finalVal.trim()) {{
                            document.getElementById('statusMsg').innerHTML = "<span style='color:#10B981;'>✅ Speech recognized! You can review/edit the text above or type in chat input.</span>";
                        }}
                    }};
                }}

                function toggleRecognition() {{
                    if (!recognition) return;
                    if (isListening) {{
                        recognition.stop();
                    }} else {{
                        document.getElementById('transcriptInput').value = '';
                        recognition.lang = lang;
                        recognition.start();
                    }}
                }}
            </script>
        </body>
        </html>
    """, height=100)

    # Chat Actions (Clear / New Chat)
    c1, c2, c3 = st.columns([4, 1, 1])
    with c2:
        if st.button("🗑️ Clear Chat"):
            clear_chat_history(user_id=user_id)
            st.rerun()
    with c3:
        if st.button("✨ New Chat"):
            clear_chat_history(user_id=user_id)
            st.rerun()
            
    # Standard Chat Input Box
    user_input = st.chat_input("Ask CareerMate AI a question (type or send voice text)...")
    final_query = prompt_to_send if prompt_to_send else user_input
    
    if final_query:
        if final_query.strip():
            with st.spinner("CareerMate AI is analyzing dataset and generating recommendation..."):
                process_chat_message(user_message=final_query, user_id=user_id, user_skills=user_skills_str)
            st.rerun()

if __name__ == "__main__":
    render_chat_page()

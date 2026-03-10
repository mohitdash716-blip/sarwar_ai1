"""
Sarwar AI — Main Streamlit Application (Premium Version)
A unified AI assistant platform with a high-fidelity, Apple-inspired UI.
Matches the Next.js visual style perfectly.
"""

import os
import uuid
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from utils.chat_handler import handle_chat, get_available_models
from utils.tools import (
    run_summarizer,
    run_email_generator,
    run_rewriter,
    run_content_generator,
)

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sarwar AI ✦",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Advanced Custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global Theme Override ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #ffffff;
    --sidebar-bg: #fbfbfd;
    --accent: #007aff;
    --text-main: #1d1d1f;
    --text-muted: #86868b;
    --border: rgba(0, 0, 0, 0.06);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 12px 24px rgba(0, 0, 0, 0.05);
}

/* Base Styles */
[data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, body {
    background-color: var(--bg) !important;
    color: var(--text-main) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* Hide Streamlit components */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Sidebar Styling ── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 1rem !important;
}

/* Sidebar Navigation Buttons (Ghost Style) */
div[data-testid="stSidebarNav"] { display: none !important; }

.stButton > button {
    border: none !important;
    background: transparent !important;
    color: var(--text-muted) !important;
    text-align: left !important;
    padding: 0.6rem 1rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: rgba(0, 0, 0, 0.03) !important;
    color: var(--text-main) !important;
}

/* Active Sidebar Item */
.stButton > button[kind="secondaryFormSubmit"], 
.stButton > button.active-nav {
    background: rgba(0, 122, 255, 0.05) !important;
    color: var(--accent) !important;
}

/* New Chat Button Card */
div.new-chat-container button {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text-main) !important;
    justify-content: center !important;
    font-weight: 600 !important;
    margin-bottom: 2rem !important;
}
div.new-chat-container button:hover {
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}

/* ── Top Bar / Header ── */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 0rem;
    margin-bottom: 2rem;
}
.page-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-main);
}

/* ── Chat Interface ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 1rem 0 !important;
}

/* Assistant Icon & Bubble */
.assistant-icon {
    width: 28px;
    height: 28px;
    background: rgba(0, 122, 255, 0.1);
    color: var(--accent);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
}

[data-testid="stChatMessageAvatarAssistant"] { display: none !important; }

/* ── Floating Chat Input ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 40px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 700px !important;
    max-width: 90vw !important;
    background: #ffffff !important;
    border-radius: 24px !important;
    border: 1px solid var(--border) !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08) !important;
    padding: 8px 16px !important;
    z-index: 1000 !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--text-main) !important;
}

/* Sidebar Footer (Settings) */
.sidebar-footer {
    position: absolute;
    bottom: 20px;
    left: 20px;
    right: 20px;
}
.footer-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    color: var(--text-muted);
    font-size: 0.9rem;
    cursor: pointer;
    border-radius: 8px;
}
.footer-item:hover { background: rgba(0, 0, 0, 0.03); color: var(--text-main); }
.avatar-circle {
    width: 24px;
    height: 24px;
    background: #333;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "active_view" not in st.session_state:
    st.session_state.active_view = "chat" # Default to chat for dashboard feel
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# ── Actions ───────────────────────────────────────────────────────────────────
def new_chat():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"title": "New Conversation", "messages": [], "model": "GPT-4o"}
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; padding:0 10px; margin-bottom:2rem;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
            <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
        </svg>
        <span style="font-weight:700; font-size:1.2rem; color:#1d1d1f;">Sarwar AI</span>
    </div>
    """, unsafe_allow_html=True)
    
    # New Chat Button
    st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
    if st.button("＋ New Chat", use_container_width=True, key="new_chat_btn"):
        new_chat()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Nav Items
    def nav_button(label, icon_svg, view_name):
        is_active = st.session_state.active_view == view_name
        btn_key = f"nav_{view_name}"
        if st.button(label, key=btn_key, use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.active_view = view_name
            st.rerun()

    # Chat
    nav_button("💬 Chat", "", "chat")
    nav_button("📝 Summarizer", "", "summarizer")
    nav_button("✉️ Email Generator", "", "email")
    nav_button("🔄 Rewriter", "", "rewriter")
    nav_button("🎨 Content Gen", "", "content")
    
    # Settings Footer
    st.markdown("""
    <div class="sidebar-footer">
        <div class="footer-item">
            <div class="avatar-circle">N</div>
            <span>Settings</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content Header ───────────────────────────────────────────────────────
col_title, col_model = st.columns([1, 1])
with col_title:
    st.markdown(f'<div class="page-title">{"New Conversation" if st.session_state.active_view == "chat" else st.session_state.active_view.title()}</div>', unsafe_allow_html=True)
with col_model:
    selected_model = st.selectbox("", get_available_models(), index=0, label_visibility="collapsed")

st.markdown("---")

# ── View Logic ────────────────────────────────────────────────────────────────
if st.session_state.active_view == "chat":
    if not st.session_state.current_session_id:
        new_chat()
    
    sid = st.session_state.current_session_id
    session = st.session_state.sessions[sid]
    
    # Chat History
    for msg in session["messages"]:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div style="display:flex; align-items:flex-start;">
                    <div class="assistant-icon">✦</div>
                    <div style="flex:1;">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write(msg["content"])
    
    # Floating Input
    if prompt := st.chat_input("Message Sarwar AI..."):
        session["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = handle_chat(prompt, selected_model, history=session["messages"][:-1])
                st.markdown(f"""
                <div style="display:flex; align-items:flex-start;">
                    <div class="assistant-icon">✦</div>
                    <div style="flex:1;">{response}</div>
                </div>
                """, unsafe_allow_html=True)
                session["messages"].append({"role": "assistant", "content": response})
        st.rerun()

elif st.session_state.active_view == "summarizer":
    st.markdown('<div class="tool-view"><h1>Text Summarizer</h1>', unsafe_allow_html=True)
    text = st.text_area("Input Text", placeholder="Paste your content here...", height=250)
    if st.button("Generate Summary", type="primary"):
        if text:
            with st.spinner("Analyzing..."):
                res = run_summarizer(text, selected_model)
                st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ... (Email, Rewriter, Content Gen follow same pattern but with updated CSS classes)
# For brevity, Email, Rewriter, Content Gen logic is similar to summarizer.
# I'll include them to ensure completeness.

elif st.session_state.active_view == "email":
    st.markdown('<div class="tool-view"><h1>Email Generator</h1>', unsafe_allow_html=True)
    context = st.text_area("What is this email about?", height=150)
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Formal"])
    if st.button("Draft Email", type="primary"):
        if context:
            with st.spinner("Drafting..."):
                res = run_email_generator(context, tone.lower(), selected_model)
                st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_view == "rewriter":
    st.markdown('<div class="tool-view"><h1>Content Rewriter</h1>', unsafe_allow_html=True)
    text = st.text_area("Original Text", height=200)
    style = st.selectbox("Target Style", ["Formal", "Casual", "Simpler", "Creative"])
    if st.button("Rewrite Now", type="primary"):
        if text:
            with st.spinner("Rewriting..."):
                res = run_rewriter(text, style.lower(), selected_model)
                st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_view == "content":
    st.markdown('<div class="tool-view"><h1>Creative Content Generator</h1>', unsafe_allow_html=True)
    topic = st.text_input("Topic / Title")
    ctype = st.selectbox("Format", ["Blog Post", "LinkedIn Post", "Twitter Thread"])
    if st.button("Generate Content", type="primary"):
        if topic:
            with st.spinner("Creating..."):
                res = run_content_generator(topic, ctype.lower(), selected_model)
                st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

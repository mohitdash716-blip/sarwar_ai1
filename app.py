"""
Sarwar AI — Main Streamlit Application (Premium Version)
A unified AI assistant platform with a high-fidelity, Apple-inspired UI.
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
    page_title="Sarwar AI ✦ Premium",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Apple-Inspired Premium Theme (Forced Light Mode) ── */

:root {
    --bg: #fbfbfd;
    --fg: #1d1d1f;
    --accent: #007aff;
    --glass: rgba(255, 255, 255, 0.72);
    --border: rgba(0, 0, 0, 0.08);
    --shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
    --card: #ffffff;
}

/* Force Light Theme Colors */
[data-testid="stAppViewContainer"], 
[data-testid="stHeader"], 
.main,
body {
    background-color: var(--bg) !important;
    color: var(--fg) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

/* Hide Streamlit elements */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--glass) !important;
    backdrop-filter: blur(40px) !important;
    -webkit-backdrop-filter: blur(40px) !important;
    border-right: 1px solid var(--border) !important;
    width: 300px !important;
}

/* ── Landing Page (Hero) ── */
.hero-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 85vh;
    text-align: center;
    background: radial-gradient(circle at center, #ffffff 0%, #fbfbfd 100%);
}
.hero-title {
    font-size: clamp(3rem, 10vw, 6rem);
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1.05;
    background: linear-gradient(180deg, #1d1d1f 60%, #86868b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem;
}
.hero-subtitle {
    font-size: clamp(1.1rem, 2vw, 1.5rem);
    color: #86868b;
    max-width: 600px;
    margin-bottom: 3rem;
    line-height: 1.5;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    background: #ffffff !important;
    color: var(--fg) !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: #000 !important;
    color: #fff !important;
    border: none !important;
}

/* ── Chat Header ── */
.chat-header {
    padding: 1rem 2rem;
    background: var(--glass);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 100;
    display: flex; align-items: center; justify-content: space-between;
}

/* ── Message Bubbles ── */
[data-testid="stChatMessage"] {
    padding: 1.2rem !important;
    margin-bottom: 1rem !important;
    border-radius: 20px !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #000 !important; color: #fff !important;
    margin-left: 10% !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: #fff !important; color: #1d1d1f !important;
    border: 1px solid var(--border) !important;
    margin-right: 10% !important;
    box-shadow: var(--shadow) !important;
}

/* Tool Cards */
.tool-view {
    padding: 2rem 15%;
}
.output-box {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow: var(--shadow);
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "active_view" not in st.session_state:
    st.session_state.active_view = "landing"
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# ── Actions ──
def start_app():
    st.session_state.active_view = "chat"

def new_chat():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"title": "New Chat", "messages": [], "model": "GPT-4o"}
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"

# ── Views ──

if st.session_state.active_view == "landing":
    st.markdown("""
<div class="hero-wrapper">
    <div style="background:rgba(0,122,255,0.1); color:#007aff; padding:6px 16px; border-radius:30px; font-size:0.85rem; font-weight:600; margin-bottom:2rem;">
        Presenting Sarwar AI ✦
    </div>
    <h1 class="hero-title">Intelligence,<br>refined.</h1>
    <p class="hero-subtitle">Experience the world's most powerful AI models in a unified, premium interface designed for clarity and speed.</p>
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Enter Sarwar AI ✦", key="enter_btn", use_container_width=True, kind="primary"):
            start_app()
            st.rerun()

else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h2 style='padding:0 10px; margin-bottom:1.5rem;'>Sarwar AI ✦</h2>", unsafe_allow_html=True)
        if st.button("＋ New Chat", use_container_width=True):
            new_chat()
            st.rerun()
            
        st.markdown("---")
        st.markdown("### Navigation")
        if st.button("💬 Chat Dashboard", use_container_width=True, type="primary" if st.session_state.active_view == "chat" else "secondary"):
            st.session_state.active_view = "chat"
            st.rerun()
        if st.button("📝 Text Summarizer", use_container_width=True, type="primary" if st.session_state.active_view == "summarizer" else "secondary"):
            st.session_state.active_view = "summarizer"
            st.rerun()
        if st.button("✉️ Email Generator", use_container_width=True, type="primary" if st.session_state.active_view == "email" else "secondary"):
            st.session_state.active_view = "email"
            st.rerun()
        if st.button("🔄 Content Rewriter", use_container_width=True, type="primary" if st.session_state.active_view == "rewriter" else "secondary"):
            st.session_state.active_view = "rewriter"
            st.rerun()
        if st.button("🎨 Creative Content", use_container_width=True, type="primary" if st.session_state.active_view == "content" else "secondary"):
            st.session_state.active_view = "content"
            st.rerun()
            
        st.markdown("---")
        selected_model = st.selectbox("Intelligence Model", get_available_models(), index=0)
        
        st.markdown("---")
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.active_view = "landing"
            st.rerun()

    # View Logic
    if st.session_state.active_view == "chat":
        if not st.session_state.current_session_id:
            new_chat()
        
        sid = st.session_state.current_session_id
        session = st.session_state.sessions[sid]
        
        st.markdown(f'<div class="chat-header"><span style="font-weight:700;">Chat</span><span style="background:rgba(0,122,255,0.1); color:#007aff; padding:2px 10px; border-radius:20px; font-size:0.75rem;">{selected_model}</span></div>', unsafe_allow_html=True)
        
        for msg in session["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        if prompt := st.chat_input("Ask Sarwar AI anything..."):
            session["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = handle_chat(prompt, selected_model, history=session["messages"][:-1])
                    st.write(response)
                    session["messages"].append({"role": "assistant", "content": response})
            st.rerun()

    elif st.session_state.active_view == "summarizer":
        st.markdown('<div class="tool-view"><h1>Text Summarizer</h1>', unsafe_allow_html=True)
        text = st.text_area("Input Text", placeholder="Paste your content here...", height=250)
        if st.button("Generate Summary", kind="primary"):
            if text:
                with st.spinner("Analyzing..."):
                    res = run_summarizer(text, selected_model)
                    st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_view == "email":
        st.markdown('<div class="tool-view"><h1>Email Generator</h1>', unsafe_allow_html=True)
        context = st.text_area("What is this email about?", height=150)
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Formal"])
        if st.button("Draft Email", kind="primary"):
            if context:
                with st.spinner("Drafting..."):
                    res = run_email_generator(context, tone.lower(), selected_model)
                    st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_view == "rewriter":
        st.markdown('<div class="tool-view"><h1>Content Rewriter</h1>', unsafe_allow_html=True)
        text = st.text_area("Original Text", height=200)
        style = st.selectbox("Target Style", ["Formal", "Casual", "Simpler", "Creative"])
        if st.button("Rewrite Now", kind="primary"):
            if text:
                with st.spinner("Rewriting..."):
                    res = run_rewriter(text, style.lower(), selected_model)
                    st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.active_view == "content":
        st.markdown('<div class="tool-view"><h1>Creative Content Generator</h1>', unsafe_allow_html=True)
        topic = st.text_input("Topic / Title")
        ctype = st.selectbox("Format", ["Blog Post", "LinkedIn Post", "Twitter Thread"])
        if st.button("Generate Content", kind="primary"):
            if topic:
                with st.spinner("Creating..."):
                    res = run_content_generator(topic, ctype.lower(), selected_model)
                    st.markdown(f'<div class="output-box">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

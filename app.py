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
    initial_sidebar_state="collapsed", # Better for Landing Page
)

# ── Advanced Custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global Theme Override ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #ffffff;
    --sidebar-bg: #fbfbfd;
    --accent: #007aff;
    --text-main: #1d1d1f;
    --text-muted: #86868b;
    --border: rgba(0, 0, 0, 0.06);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 12px 32px rgba(0, 0, 0, 0.08);
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

/* ── Landing Page Header ── */
.landing-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 5%;
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 1000;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
}

.go-to-app {
    color: var(--text-main);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
}

/* ── Hero Section ── */
.hero-container {
    padding-top: 15vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    max-width: 900px;
    margin: 0 auto;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 30px;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}

.badge-dot {
    width: 6px;
    height: 6px;
    background-color: var(--accent);
    border-radius: 50%;
}

.hero-title-main {
    font-size: clamp(3rem, 7vw, 5rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
    color: var(--text-main);
    margin-bottom: 1.5rem;
}

.hero-title-main span {
    color: var(--accent);
}

.hero-subtitle-main {
    font-size: 1.25rem;
    color: var(--text-muted);
    max-width: 650px;
    margin-bottom: 3.5rem;
    line-height: 1.6;
    font-weight: 500;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 30px !important;
    padding: 0.8rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: 1px solid var(--border) !important;
}

/* Primary Button (Start Chatting) */
div[data-testid="stButton"] button[kind="primary"] {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 10px 20px -5px rgba(0, 122, 255, 0.45) !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 25px -5px rgba(0, 122, 255, 0.55) !important;
}

/* Secondary Button (Explore Tools) */
div[data-testid="stButton"] button[kind="secondary"] {
    background: #ffffff !important;
    color: var(--text-main) !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    background: #fbfbfd !important;
    border-color: var(--text-main) !important;
}

/* ── Sidebar Styling (Dashboard) ── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
}

/* Sidebar Ghost Items */
.sidebar-nav-btn button {
    background: transparent !important;
    border: none !important;
    color: var(--text-muted) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    margin-bottom: 2px !important;
}

/* Active Nav */
.sidebar-nav-btn-active button {
    background: rgba(0, 122, 255, 0.06) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
}

/* ── Floating Input ── */
[data-testid="stChatInput"] {
    border-bottom: none !important;
    background: transparent !important;
}
[data-testid="stChatInput"] > div {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    box-shadow: var(--shadow-md) !important;
    max-width: 800px !important;
    margin: 0 auto 30px auto !important;
}

/* Assistant Bubble */
.assistant-reply {
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.ai-icon {
    width: 32px; height: 32px;
    background: rgba(0,122,255,0.08);
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px; color: var(--accent);
}

/* Absolute Settings Footer */
.settings-footer {
    position: absolute; bottom: 25px; left: 20px; right: 20px;
}

</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "active_view" not in st.session_state:
    st.session_state.active_view = "landing"
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# ── Actions ───────────────────────────────────────────────────────────────────
def start_app():
    st.session_state.active_view = "chat"

def new_chat():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"messages": [], "model": "GPT-4o"}
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"

# ── View: LANDING ──────────────────────────────────────────────────────────────
if st.session_state.active_view == "landing":
    # Header
    st.markdown("""
    <div class="landing-header">
        <div style="display:flex; align-items:center; gap:10px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span style="font-weight:700; font-size:1.4rem;">Sarwar AI</span>
        </div>
        <div class="go-to-app" onclick="window.parent.postMessage({type: 'streamlit:set_widget_value', key: 'goto_btn', value: true}, '*')">
            Go to App
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="badge-dot"></span>
            Everything is better in one place
        </div>
        <h1 class="hero-title-main">One interface for<br><span>multiple AI models.</span></h1>
        <p class="hero-subtitle-main">
            Experience the world's most capable models in a premium, 
            calm, and intuitive workspace designed by humans.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Buttons
    b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns([1.5, 1, 0.1, 1, 1.5])
    with b_col2:
        if st.button("Start Chatting", key="start_chat_landing", type="primary", use_container_width=True):
            start_app()
            st.rerun()
    with b_col4:
        if st.button("Explore Tools", key="explore_tools_landing", type="secondary", use_container_width=True):
            st.session_state.active_view = "summarizer"
            st.rerun()
    
    # Dummy button for Header "Go to App" javascript action
    if st.button("", key="goto_btn", help="hidden"):
        start_app()
        st.rerun()

    # Footer/Bottom Elements (like the small N avatar from photo)
    st.markdown("""
    <div style="position:fixed; bottom:20px; left:20px;">
        <div style="width:32px; height:32px; background:#1d1d1f; color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:800; box-shadow:0 4px 12px rgba(0,0,0,0.2);">
            N
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── View: DASHBOARD (Chat, Tools, etc.) ─────────────────────────────────────────
else:
    with st.sidebar:
        # Mini Logo
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:2rem; padding:0 5px;">
             <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span style="font-weight:700; font-size:1.1rem;">Sarwar AI</span>
        </div>
        """, unsafe_allow_html=True)
        
        # New Chat Card
        if st.button("＋ New Chat", key="sidebar_new_chat", use_container_width=True):
            new_chat()
            st.rerun()
        
        st.markdown("<p style='font-size:0.7rem; font-weight:800; color:#86868b; text-transform:uppercase; margin:1.5rem 0 0.5rem 5px;'>Navigation</p>", unsafe_allow_html=True)
        
        # Nav Helper
        def sidebar_nav(label, view_target):
            is_active = st.session_state.active_view == view_target
            container_class = "sidebar-nav-btn-active" if is_active else "sidebar-nav-btn"
            st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
            if st.button(label, key=f"nav_{view_target}", use_container_width=True):
                st.session_state.active_view = view_target
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        sidebar_nav("💬 Chat", "chat")
        sidebar_nav("📝 Summarizer", "summarizer")
        sidebar_nav("✉️ Email Generator", "email")
        sidebar_nav("🔄 Rewriter", "rewriter")
        sidebar_nav("🎨 Content Gen", "content")
        
        # Settings Footer
        st.markdown("""
        <div class="settings-footer">
            <div style="display:flex; align-items:center; gap:12px; cursor:pointer;">
                <div style="width:28px; height:28px; background:#1d1d1f; color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.7rem; font-weight:800;">N</div>
                <span style="font-size:0.85rem; font-weight:600; color:#1d1d1f;">Settings</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Top Content Header
    h_col1, h_col2 = st.columns([1, 1])
    with h_col1:
        st.markdown(f'<h2 style="font-size:1.2rem; font-weight:700;">{st.session_state.active_view.title() if st.session_state.active_view != "chat" else "New Conversation"}</h2>', unsafe_allow_html=True)
    with h_col2:
        selected_model = st.selectbox("Model", get_available_models(), label_visibility="collapsed")
    
    st.markdown("<hr style='border:none; border-top:1px solid rgba(0,0,0,0.05); margin:0.5rem 0 2rem 0;'>", unsafe_allow_html=True)

    # Dashboard Views
    if st.session_state.active_view == "chat":
        if not st.session_state.current_session_id:
            new_chat()
        
        sid = st.session_state.current_session_id
        session = st.session_state.sessions[sid]
        
        for msg in session["messages"]:
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant":
                    st.markdown(f'<div class="assistant-reply"><div class="ai-icon">✦</div><div>{msg["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.write(msg["content"])
        
        if prompt := st.chat_input("Message Sarwar AI..."):
            session["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Refining..."):
                    response = handle_chat(prompt, selected_model, history=session["messages"][:-1])
                    st.markdown(f'<div class="assistant-reply"><div class="ai-icon">✦</div><div>{response}</div></div>', unsafe_allow_html=True)
                    session["messages"].append({"role": "assistant", "content": response})
            st.rerun()

    elif st.session_state.active_view in ["summarizer", "email", "rewriter", "content"]:
        st.markdown(f'<div style="max-width:800px; margin:0 auto; padding:2rem 0;">', unsafe_allow_html=True)
        if st.session_state.active_view == "summarizer":
            st.markdown("<h1 style='font-size:2.5rem; font-weight:800; margin-bottom:1rem;'>Text Summarizer</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color:#86868b; font-size:1.1rem; margin-bottom:3rem;'>Distill long documents into clear, high-fidelity insights.</p>", unsafe_allow_html=True)
            text = st.text_area("Input Text", placeholder="Paste your content here...", height=250)
            if st.button("Generate Summary", type="primary"):
                if text:
                    with st.spinner("Analyzing..."):
                        res = run_summarizer(text, selected_model)
                        st.markdown(f'<div style="background:#fbfbfd; border:1px solid rgba(0,0,0,0.06); padding:2rem; border-radius:24px; margin-top:2rem; line-height:1.6;">{res}</div>', unsafe_allow_html=True)
        
        elif st.session_state.active_view == "email":
            st.markdown("<h1 style='font-size:2.5rem; font-weight:800; margin-bottom:1rem;'>Email Generator</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color:#86868b; font-size:1.1rem; margin-bottom:3rem;'>Draft perfectly toned professional emails instantly.</p>", unsafe_allow_html=True)
            context = st.text_area("Context", placeholder="What is this email about?", height=150)
            tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Formal"])
            if st.button("Draft Email", type="primary"):
                if context:
                    with st.spinner("Drafting..."):
                        res = run_email_generator(context, tone.lower(), selected_model)
                        st.markdown(f'<div style="background:#fbfbfd; border:1px solid rgba(0,0,0,0.06); padding:2rem; border-radius:24px; margin-top:2rem; line-height:1.6;">{res}</div>', unsafe_allow_html=True)

        elif st.session_state.active_view == "rewriter":
            st.markdown("<h1 style='font-size:2.5rem; font-weight:800; margin-bottom:1rem;'>Content Rewriter</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color:#86868b; font-size:1.1rem; margin-bottom:3rem;'>Refine your writing into any style while preserving meaning.</p>", unsafe_allow_html=True)
            text = st.text_area("Original Text", height=200)
            style = st.selectbox("Style", ["Academic", "Witty", "Direct", "Creative"])
            if st.button("Rewrite Now", type="primary"):
                if text:
                    with st.spinner("Rewriting..."):
                        res = run_rewriter(text, style.lower(), selected_model)
                        st.markdown(f'<div style="background:#fbfbfd; border:1px solid rgba(0,0,0,0.06); padding:2rem; border-radius:24px; margin-top:2rem; line-height:1.6;">{res}</div>', unsafe_allow_html=True)

        elif st.session_state.active_view == "content":
            st.markdown("<h1 style='font-size:2.5rem; font-weight:800; margin-bottom:1rem;'>Content Generator</h1>", unsafe_allow_html=True)
            topic = st.text_input("Topic")
            ctype = st.selectbox("Format", ["Blog Post", "LinkedIn Post", "Twitter Thread"])
            if st.button("Generate Content", type="primary"):
                if topic:
                    with st.spinner("Generating..."):
                        res = run_content_generator(topic, ctype.lower(), selected_model)
                        st.markdown(f'<div style="background:#fbfbfd; border:1px solid rgba(0,0,0,0.06); padding:2rem; border-radius:24px; margin-top:2rem; line-height:1.6;">{res}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

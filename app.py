"""
Sarwar AI — Main Streamlit Application (Premium Version)
A unified AI assistant platform with a futuristic, Apple-inspired UI.
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
    initial_sidebar_state="collapsed" if "active_view" not in st.session_state or st.session_state.active_view == "landing" else "expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Apple-Inspired Premium Light Theme (Forced) ── */

/* 
   We force light theme colors even if Streamlit is set to dark mode
   by targeting the root and specific Streamlit classes.
*/

:root {
    --st-bg: #fbfbfd;
    --st-fg: #1d1d1f;
    --st-accent: #007aff;
    --st-glass: rgba(255, 255, 255, 0.7);
    --st-border: rgba(0, 0, 0, 0.08);
    --st-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
}

/* Global Background Override */
[data-testid="stAppViewContainer"], 
[data-testid="stHeader"], 
.main,
body {
    background-color: var(--st-bg) !important;
    color: var(--st-fg) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

/* Hide Streamlit elements */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* Block Container Padding */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar Glassmorphism ── */
[data-testid="stSidebar"] {
    background: var(--st-glass) !important;
    backdrop-filter: blur(40px) !important;
    -webkit-backdrop-filter: blur(40px) !important;
    border-right: 1px solid var(--st-border) !important;
    width: 300px !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    padding-top: 2rem !important;
}

/* ── Landing Page (Hero) ── */
.hero-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: radial-gradient(circle at center, #ffffff 0%, #fbfbfd 100%);
    text-align: center;
    padding: 2rem;
    z-index: 1;
}
.hero-badge {
    background: rgba(0, 122, 255, 0.1);
    color: var(--st-accent);
    padding: 8px 20px;
    border-radius: 40px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 2.5rem;
    letter-spacing: 0.02em;
    border: 1px solid rgba(0, 122, 255, 0.05);
}
.hero-title {
    font-size: clamp(3rem, 10vw, 6rem);
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1.05;
    margin-bottom: 2rem;
    color: #1d1d1f;
    background: linear-gradient(180deg, #1d1d1f 60%, #86868b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: clamp(1.1rem, 2vw, 1.6rem);
    color: #86868b;
    max-width: 700px;
    margin-bottom: 3.5rem;
    line-height: 1.5;
    font-weight: 400;
}

/* ── Buttons ── */
.premium-btn-container {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
}
.stButton > button {
    border-radius: 14px !important;
    border: 1px solid var(--st-border) !important;
    background: #ffffff !important;
    color: var(--st-fg) !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}
.stButton > button:hover {
    border-color: var(--st-accent) !important;
    color: var(--st-accent) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.05) !important;
}
/* Primary Button Override */
div[data-testid="stButton"] button[kind="primary"] {
    background: #000 !important;
    color: #fff !important;
    border: none !important;
}

/* ── Chat Header ── */
.chat-header {
    padding: 1.5rem 2.5rem;
    background: rgba(251, 251, 253, 0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--st-border);
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.chat-viewport {
    padding: 3rem 18% 12rem 18%;
    background: transparent;
}

/* ── Message Bubbles ── */
/* User */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #000 !important;
    color: #fff !important;
    border-radius: 20px 20px 4px 20px !important;
    margin-left: 15% !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
/* Assistant */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: #fff !important;
    color: #1d1d1f !important;
    border: 1px solid var(--st-border) !important;
    border-radius: 20px 20px 20px 4px !important;
    margin-right: 15% !important;
    box-shadow: var(--st-shadow) !important;
}

/* ── Input Bar ── */
[data-testid="stChatInput"] {
    border-radius: 30px !important;
    border: 1px solid var(--st-border) !important;
    background: #fff !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.04) !important;
    padding: 6px !important;
}

/* ── Containers/Cards ── */
.output-card {
    background: #ffffff;
    border: 1px solid var(--st-border);
    border-radius: 24px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow: var(--st-shadow);
    line-height: 1.7;
}

/* Tool Header */
.tool-title {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
}

/* ── Animations ── */
@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.98) translateY(10px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-premium {
    animation: fadeInScale 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Forms */
[data-testid="stTextArea"] textarea, 
[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid var(--st-border) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}

</style>
""", unsafe_allow_html=True)
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
    st.rerun()

def new_chat():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"title": "New Chat", "messages": [], "model": "GPT-4o"}
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"

# ── Views ─────────────────────────────────────────────────────────────────────

# ── 1. Landing View ──
if st.session_state.active_view == "landing":
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-badge animate-fade-in">Presenting Sarwar AI ✦</div>
        <h1 class="hero-title animate-fade-in">Intelligence,<br>refined.</h1>
        <p class="hero-subtitle animate-fade-in">Experience the world's most powerful AI models in a unified, premium interface designed for clarity and speed.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Enter Sarwar AI ✦", key="enter_btn", use_container_width=True):
            start_app()

# ── 2. App Views (Chat & Tools) ──
else:
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='padding:0 10px;'>Sarwar AI ✦</h2>", unsafe_allow_html=True)
        if st.button("＋ New Chat", use_container_width=True):
            new_chat()
            st.rerun()
            
        st.markdown("---")
        st.markdown("### Views")
        if st.button("💬 Chat", use_container_width=True, type="primary" if st.session_state.active_view == "chat" else "secondary"):
            st.session_state.active_view = "chat"
            st.rerun()
        if st.button("📝 Summarizer", use_container_width=True, type="primary" if st.session_state.active_view == "summarizer" else "secondary"):
            st.session_state.active_view = "summarizer"
            st.rerun()
        if st.button("✉️ Email Gen", use_container_width=True, type="primary" if st.session_state.active_view == "email" else "secondary"):
            st.session_state.active_view = "email"
            st.rerun()
        if st.button("🔄 Rewriter", use_container_width=True, type="primary" if st.session_state.active_view == "rewriter" else "secondary"):
            st.session_state.active_view = "rewriter"
            st.rerun()
        if st.button("🎨 Content Gen", use_container_width=True, type="primary" if st.session_state.active_view == "content" else "secondary"):
            st.session_state.active_view = "content"
            st.rerun()
            
        st.markdown("---")
        # Model Selection
        selected_model = st.selectbox("Intelligence Model", get_available_models(), index=0)
        
        st.markdown("---")
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.active_view = "landing"
            st.rerun()

    # Main Content
    if st.session_state.active_view == "chat":
        if not st.session_state.current_session_id:
            new_chat()
            
        sid = st.session_state.current_session_id
        session = st.session_state.sessions[sid]
        
        st.markdown(f"""
        <div class="chat-header">
            <span style="font-weight:700; font-size:1.2rem;">Chat</span>
            <span class="hero-badge" style="margin-bottom:0;">{selected_model}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='chat-viewport'>", unsafe_allow_html=True)
        for msg in session["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        st.markdown("</div>", unsafe_allow_html=True)
        
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
        st.markdown("<h1 style='padding:2rem 15% 0 15%;'>Text Summarizer</h1>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div style='padding:0 15%;'>", unsafe_allow_html=True)
            text = st.text_area("Input Text", placeholder="Paste your content here...", height=250)
            if st.button("Summarize Now", type="primary"):
                if text:
                    with st.spinner("Analyzing..."):
                        res = run_summarizer(text, selected_model)
                        st.markdown(f"<div class='output-card'>{res}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.active_view == "email":
        st.markdown("<h1 style='padding:2rem 15% 0 15%;'>Email Generator</h1>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div style='padding:0 15%;'>", unsafe_allow_html=True)
            context = st.text_area("What is this email about?", height=150)
            tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Formal"])
            if st.button("Generate Draft", type="primary"):
                if context:
                    with st.spinner("Drafting..."):
                        res = run_email_generator(context, tone.lower(), selected_model)
                        st.markdown(f"<div class='output-card'>{res}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.active_view == "rewriter":
        st.markdown("<h1 style='padding:2rem 15% 0 15%;'>Content Rewriter</h1>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div style='padding:0 15%;'>", unsafe_allow_html=True)
            text = st.text_area("Original Text", height=200, key="rewriter_input_area")
            style = st.selectbox("Target Style", ["Formal", "Casual", "Simpler", "Creative"], key="rewriter_style_select")
            if st.button("Rewrite Content", type="primary", key="rewriter_submit"):
                if text:
                    with st.spinner("Rewriting..."):
                        res = run_rewriter(text, style.lower(), selected_model)
                        st.markdown(f"<div class='output-card'>{res}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.active_view == "content":
        st.markdown("<h1 style='padding:2rem 15% 0 15%;'>Content Creator</h1>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div style='padding:0 15%;'>", unsafe_allow_html=True)
            topic = st.text_input("Topic / Title", key="content_topic_input")
            ctype = st.selectbox("Format", ["Blog Post", "LinkedIn Post", "Twitter Thread"], key="content_type_select")
            if st.button("Create Content", type="primary", key="content_submit"):
                if topic:
                    with st.spinner("Creating..."):
                        res = run_content_generator(topic, ctype.lower(), selected_model)
                        st.markdown(f"<div class='output-card'>{res}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

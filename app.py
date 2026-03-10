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
/* ── Apple Inspired Minimalist Light Theme ── */

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: #f5f5f7;
    color: #1d1d1f;
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border-right: 1px solid rgba(0, 0, 0, 0.05);
    width: 280px !important;
}

/* ── Landing Page ── */
.hero-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 90vh;
    background: radial-gradient(circle at center, #ffffff 0%, #f5f5f7 100%);
    text-align: center;
    padding: 2rem;
}
.hero-badge {
    background: rgba(0, 122, 255, 0.08);
    color: #007aff;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 2rem;
    letter-spacing: 0.02em;
}
.hero-title {
    font-size: 5rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    background: linear-gradient(180deg, #1d1d1f 0%, #434343 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 1.5rem;
    color: #86868b;
    max-width: 600px;
    margin-bottom: 3rem;
    line-height: 1.4;
}

/* ── Dashboard UI ── */
.chat-header {
    padding: 1.2rem 2rem;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(0,0,0,0.05);
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.chat-viewport {
    padding: 2rem 15% 10rem 15%;
}

/* ── Animations ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
    animation: fadeIn 0.8s ease-out forwards;
}

/* ── Buttons ── */
.premium-btn {
    background: #000000;
    color: #ffffff !important;
    padding: 12px 32px;
    border-radius: 30px;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}
.premium-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

/* ── Tool Headers ── */
.tool-header-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

/* ── Tool output ── */
.output-card {
    background: rgba(0, 122, 255, 0.03);
    border: 1px solid rgba(0, 122, 255, 0.1);
    border-radius: 18px;
    padding: 1.5rem;
    color: #1d1d1f;
    line-height: 1.6;
    margin-top: 1.5rem;
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

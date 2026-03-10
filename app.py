"""
Sarwar AI — Main Streamlit Application (Unified Premium Version - Final Fix)
A unified AI assistant platform with a high-fidelity, Apple-inspired UI.
Optimized for Streamlit Cloud to ensure a perfect 1:1 match with localhost.
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

# ── Session State ─────────────────────────────────────────────────────────────
if "active_view" not in st.session_state:
    st.session_state.active_view = "landing"
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# Actions
def new_chat():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"messages": [], "model": "GPT-4o"}
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"

def start_app():
    if not st.session_state.current_session_id:
        new_chat()
    st.session_state.active_view = "chat"

# ── Advanced Custom CSS ────────────────────────────────────────────────────────
is_landing = st.session_state.active_view == "landing"

st.markdown(f"""
<style>
/* ── Global Theme Override ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --bg: #ffffff;
    --sidebar-bg: #fbfbfd;
    --accent: #007aff;
    --text-main: #1d1d1f;
    --text-muted: #86868b;
    --border: rgba(0, 0, 0, 0.08);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 12px 32px rgba(0, 0, 0, 0.08);
}}

/* Base Styles */
[data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, body {{
    background-color: var(--bg) !important;
    color: var(--text-main) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}}

/* Hide Streamlit components */
#MainMenu, footer, header {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}

/* ── Conditional Sidebar Hiding ── */
{'div[data-testid="stSidebar"] { display: none !important; }' if is_landing else ''}
{'div[data-testid="stSidebarNav"] { display: none !important; }' if is_landing else ''}

/* ── Landing Page Header ── */
.landing-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 5.5%;
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 10000;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
}}

/* ── Button Specific Targeting (Robust Fix) ── */

/* 1. Header "Go to App" Button Styling */
div.header-btn div[data-testid="stButton"] button {{
    background: transparent !important;
    border: none !important;
    color: var(--text-main) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0 !important;
    box-shadow: none !important;
}}

/* 2. Hero Primary Button (Start Chatting) */
div.hero-primary div[data-testid="stButton"] button {{
    background: var(--accent) !important;
    color: #ffffff !important;
    border-radius: 30px !important;
    padding: 0.8rem 2.8rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    box-shadow: 0 10px 20px -5px rgba(0, 122, 255, 0.4) !important;
    transition: all 0.2s ease !important;
}}
div.hero-primary div[data-testid="stButton"] button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 25px -5px rgba(0, 122, 255, 0.5) !important;
}}

/* 3. Hero Secondary Button (Explore Tools) */
div.hero-secondary div[data-testid="stButton"] button {{
    background: #ffffff !important;
    color: var(--text-main) !important;
    border-radius: 30px !important;
    padding: 0.8rem 2.8rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}}

/* ── Hero Section ── */
.hero-container {{
    padding-top: 18vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    max-width: 950px;
    margin: 0 auto;
}}
.hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 18px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 30px;
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.badge-dot {{
    width: 6px; height: 6px;
    background-color: var(--accent);
    border-radius: 50%;
}}
.hero-title-main {{
    font-size: clamp(3.5rem, 8vw, 5.5rem);
    font-weight: 800;
    letter-spacing: -0.045em;
    line-height: 1.05;
    color: var(--text-main);
    margin-bottom: 1.8rem;
}}
.hero-title-main span {{ color: var(--accent); }}
.hero-subtitle-main {{
    font-size: 1.3rem;
    color: var(--text-muted);
    max-width: 700px;
    margin-bottom: 4rem;
    line-height: 1.6;
    font-weight: 500;
}}

/* ── Dashboard Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
}}

/* Ghost Sidebar Buttons */
div.sidebar-nav div[data-testid="stButton"] button {{
    background: transparent !important;
    border: none !important;
    color: var(--text-muted) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    margin-bottom: 4px !important;
}}
div.sidebar-nav-active div[data-testid="stButton"] button {{
    background: rgba(0, 122, 255, 0.07) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
}}

/* New Chat Card */
div.stButton > button[key="new_chat_card"] {{
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text-main) !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    padding: 0.9rem !important;
    margin: 1.5rem 0 !important;
}}

/* Floating Chat Bar */
[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 50px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(850px, 92vw) !important;
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    box-shadow: 0 15px 50px rgba(0,0,0,0.1) !important;
    border-radius: 20px !important;
    z-index: 1000 !important;
}}

/* Disclaimer */
.disclaimer {{
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.72rem;
    color: var(--text-muted);
    text-align: center;
    width: 100%;
    pointer-events: none;
}}

/* Assistant Icon */
.ai-avatar {{
    width: 32px; height: 32px;
    background: rgba(0, 122, 255, 0.1);
    color: var(--accent);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}}

</style>
""", unsafe_allow_html=True)

# ── View Logic ───────────────────────────────────────────────────────────────

if st.session_state.active_view == "landing":
    # Custom Header
    st.markdown("""
    <div class="landing-header">
        <div style="display:flex; align-items:center; gap:12px;">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span style="font-weight:800; font-size:1.5rem; letter-spacing:-0.02em;">Sarwar AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Real Header Button (Native Streamlit)
    h_col1, h_col2 = st.columns([10, 1])
    with h_col2:
        st.markdown('<div class="header-btn" style="position:fixed; top:20px; right:5.5%; z-index:10001;">', unsafe_allow_html=True)
        if st.button("Go to App", key="nav_goto_app"):
            start_app()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge"><span class="badge-dot"></span>EVERYTHING IS BETTER IN ONE PLACE</div>
        <h1 class="hero-title-main">One interface for<br><span>multiple AI models.</span></h1>
        <p class="hero-subtitle-main">Experience the world's most capable models in a premium, calm, and intuitive workspace designed by humans for thinkers.</p>
    </div>
    """, unsafe_allow_html=True)

    # Hero Buttons
    b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns([1.8, 1, 0.15, 1, 1.8])
    with b_col2:
        st.markdown('<div class="hero-primary">', unsafe_allow_html=True)
        if st.button("Start Chatting", key="start_chat_hero"):
            start_app()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with b_col4:
        st.markdown('<div class="hero-secondary">', unsafe_allow_html=True)
        if st.button("Explore Tools", key="explore_tools_hero"):
            st.session_state.active_view = "summarizer"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer Avatar
    st.markdown('<div style="position:fixed; bottom:25px; left:25px;"><div style="width:36px; height:36px; background:#1d1d1f; color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.85rem; font-weight:800; box-shadow:0 6px 15px rgba(0,0,0,0.2);">N</div></div>', unsafe_allow_html=True)

else:
    # ── Dashboard (Sidebar & Header) ──────────────────────────────────────────
    with st.sidebar:
        # Mini Logo
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem; padding:0 5px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                    <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
                </svg>
                <span style="font-weight:700; font-size:1.15rem; color:#1d1d1f;">Sarwar AI</span>
            </div>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="cursor:pointer;"><path d="m15 18-6-6 6-6"/></svg>
        </div>
        """, unsafe_allow_html=True)

        if st.button("＋ New Chat", key="new_chat_card", use_container_width=True):
            new_chat()
            st.rerun()

        st.markdown("<p style='font-size:0.75rem; font-weight:800; color:#86868b; text-transform:uppercase; margin:1.8rem 0 0.8rem 10px; letter-spacing:0.04em;'>Platform</p>", unsafe_allow_html=True)

        def dash_nav_btn(label, target, icon_sym):
            is_active = st.session_state.active_view == target
            wrap = "sidebar-nav-active" if is_active else "sidebar-nav"
            st.markdown(f'<div class="{wrap}">', unsafe_allow_html=True)
            if st.button(f"{icon_sym} {label}", key=f"btn_nav_{target}", use_container_width=True):
                st.session_state.active_view = target
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        dash_nav_btn("Chat", "chat", "💬")
        dash_nav_btn("Summarizer", "summarizer", "📝")
        dash_nav_btn("Email Generator", "email", "✉️")
        dash_nav_btn("Rewriter", "rewriter", "🔄")
        dash_nav_btn("Content Gen", "content", "🎨")

        # Sidebar Footer
        st.markdown("""
        <div style="position:absolute; bottom:30px; left:20px; right:20px; display:flex; align-items:center; gap:12px; padding:12px; cursor:pointer;">
            <div style="width:30px; height:30px; background:#1d1d1f; color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:800;">N</div>
            <span style="font-size:0.9rem; font-weight:600; color:#1d1d1f; opacity:0.9;">Settings</span>
        </div>
        """, unsafe_allow_html=True)

    # Content Top Bar
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:1.4rem 2.5rem; border-bottom:1px solid var(--border); margin-bottom:2.5rem;">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="color:#007aff;"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg></div>
            <span style="font-weight:700; font-size:1.05rem;">{st.session_state.active_view.title() if st.session_state.active_view != "chat" else "New Conversation"}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model Selector
    st.markdown('<div style="position:fixed; top:25px; right:45px; z-index:10001; width:130px;">', unsafe_allow_html=True)
    selected_model = st.selectbox("", get_available_models(), key="global_model_sel", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Views ──
    if st.session_state.active_view == "chat":
        if not st.session_state.current_session_id: new_chat()
        sid = st.session_state.current_session_id
        session = st.session_state.sessions[sid]
        
        if not session["messages"]:
            st.markdown('<div class="assistant-container"><div class="ai-avatar">✦</div><div style="padding-top:4px; font-weight:500;">Hello! I\'m Sarwar AI. How can I assist you today?</div></div>', unsafe_allow_html=True)
        
        for msg in session["messages"]:
            with st.chat_message(msg["role"]):
                if msg["role"] == "assistant":
                    st.markdown(f'<div class="assistant-container"><div class="ai-avatar">✦</div><div style="flex:1;">{msg["content"]}</div></div>', unsafe_allow_html=True)
                else: st.markdown(f'<div style="padding-left:48px;">{msg["content"]}</div>', unsafe_allow_html=True)

        if prompt := st.chat_input("Message Sarwar AI..."):
            session["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(f'<div style="padding-left:48px;">{prompt}</div>', unsafe_allow_html=True)
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    res = handle_chat(prompt, selected_model, history=session["messages"][:-1])
                    st.markdown(f'<div class="assistant-container"><div class="ai-avatar">✦</div><div style="flex:1;">{res}</div></div>', unsafe_allow_html=True)
                    session["messages"].append({"role": "assistant", "content": res})
            st.rerun()

        st.markdown('<div class="disclaimer">Sarwar AI can make mistakes. Verify important information.</div>', unsafe_allow_html=True)

    elif st.session_state.active_view == "summarizer":
        st.markdown("<div style='max-width:850px; margin:0 auto; padding:2rem 0;'><h1 style='font-size:3rem; font-weight:800; letter-spacing:-0.03em;'>Text Summarizer</h1><p style='color:#86868b; font-size:1.2rem; margin-bottom:4rem;'>Distill complex documents into high-fidelity actionable insights.</p>", unsafe_allow_html=True)
        text = st.text_area("Input Text", height=300, placeholder="Paste long-form content here...")
        st.markdown('<div class="hero-primary" style="width:200px;">', unsafe_allow_html=True)
        if st.button("Generate Summary", key="sum_gen_btn"):
            if text:
                with st.spinner("Synthesizing..."):
                    res = run_summarizer(text, selected_model)
                    st.markdown(f'<div style="background:#fbfbfd; border:1px solid var(--border); padding:2.5rem; border-radius:28px; margin-top:2.5rem; line-height:1.7;">{res}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    elif st.session_state.active_view == "email":
        st.markdown("<div style='max-width:850px; margin:0 auto; padding:2rem 0;'><h1 style='font-size:3rem; font-weight:800;'>Email Generator</h1><p style='color:#86868b; margin-bottom:4rem;'>Draft perfectly toned professional communications in seconds.</p>", unsafe_allow_html=True)
        ctx = st.text_area("Context", height=150, placeholder="What is the objective?")
        tone = st.selectbox("Desired Tone", ["Professional", "Friendly", "Urgent", "Formal"])
        st.markdown('<div class="hero-primary" style="width:200px;">', unsafe_allow_html=True)
        if st.button("Draft Email", key="email_gen_btn"):
            if ctx:
                with st.spinner("Drafting..."):
                    res = run_email_generator(ctx, tone.lower(), selected_model)
                    st.markdown(f'<div style="background:#fbfbfd; border:1px solid var(--border); padding:2.5rem; border-radius:28px; margin-top:2.5rem; line-height:1.7;">{res}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    elif st.session_state.active_view == "rewriter":
        st.markdown("<div style='max-width:850px; margin:0 auto; padding:2rem 0;'><h1 style='font-size:3rem; font-weight:800;'>Content Rewriter</h1><p style='color:#86868b;'>Refine your narrative into any style while preserving core intent.</p>", unsafe_allow_html=True)
        text = st.text_area("Original Text", height=200)
        style = st.selectbox("Target Style", ["Academic", "Witty", "Direct", "Creative"])
        st.markdown('<div class="hero-primary" style="width:200px;">', unsafe_allow_html=True)
        if st.button("Rewrite Content", key="rw_gen_btn"):
            if text:
                with st.spinner("Polishing..."):
                    res = run_rewriter(text, style.lower(), selected_model)
                    st.markdown(f'<div style="background:#fbfbfd; border:1px solid var(--border); padding:2.5rem; border-radius:28px; margin-top:2.5rem;">{res}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    elif st.session_state.active_view == "content":
        st.markdown("<div style='max-width:850px; margin:0 auto; padding:2rem 0;'><h1 style='font-size:3rem; font-weight:800;'>Content Creator</h1><p style='color:#86868b;'>Generate high-engagement social and web content instantly.</p>", unsafe_allow_html=True)
        topic = st.text_input("Topic or Prompt")
        ctype = st.selectbox("Format", ["Blog Post", "LinkedIn Post", "Twitter Thread"])
        st.markdown('<div class="hero-primary" style="width:200px;">', unsafe_allow_html=True)
        if st.button("Create Content", key="cont_gen_btn"):
            if topic:
                with st.spinner("Authoring..."):
                    res = run_content_generator(topic, ctype.lower(), selected_model)
                    st.markdown(f'<div style="background:#fbfbfd; border:1px solid var(--border); padding:2.5rem; border-radius:28px; margin-top:2.5rem;">{res}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

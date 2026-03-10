"""
Sarwar AI — Final Definitive Version
Fixes: ghost sidebar, white chat input, proper model selector positioning.
"""

import os
import uuid
import streamlit as st
from dotenv import load_dotenv

from utils.chat_handler import handle_chat, get_available_models
from utils.tools import (
    run_summarizer,
    run_email_generator,
    run_rewriter,
    run_content_generator,
)

load_dotenv()

st.set_page_config(
    page_title="Sarwar AI ✦",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session State ────────────────────────────────────────────────────────────
if "active_view" not in st.session_state:
    st.session_state.active_view = "landing"
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

def new_chat():
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"messages": [], "model": "GPT-4o"}
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"

def start_app():
    if not st.session_state.current_session_id:
        new_chat()
    st.session_state.active_view = "chat"

is_landing = st.session_state.active_view == "landing"

# ── Core CSS Injection ───────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{ font-family: 'Inter', -apple-system, sans-serif !important; box-sizing: border-box; }}

/* Full background white */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stHeader"], .stApp, .main {{
    background-color: #ffffff !important;
    color: #1d1d1f !important;
}}

/* Remove Streamlit UI clutter */
#MainMenu, footer, header, [data-testid="stDecoration"],
.stDeployButton {{ visibility: hidden !important; display: none !important; }}

/* Remove default block padding */
.block-container {{ padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }}

/* ── LANDING: Hide sidebar completely ── */
{'''
[data-testid="stSidebar"], [data-testid="stSidebarNav"] {
    display: none !important;
    width: 0 !important;
}
''' if is_landing else ''}

/* ============================================================
   SIDEBAR STYLES (Dashboard Only)
   ============================================================ */
[data-testid="stSidebar"] {{
    background: #fbfbfd !important;
    border-right: 1px solid rgba(0,0,0,0.06) !important;
}}
[data-testid="stSidebar"] .block-container {{
    padding: 1.5rem 1rem !important;
}}

/* Ghost ALL sidebar buttons - force transparent over dark Streamlit defaults */
[data-testid="stSidebar"] button {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #86868b !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin: 2px 0 !important;
    transition: all 0.15s ease !important;
}}
[data-testid="stSidebar"] button:hover {{
    background: rgba(0,0,0,0.035) !important;
    color: #1d1d1f !important;
}}

/* Active sidebar state via wrapper */
div.nav-active [data-testid="stSidebar"] button,
div.nav-active button {{
    background: rgba(0, 122, 255, 0.08) !important;
    color: #007aff !important;
    font-weight: 600 !important;
}}

/* New Chat Card override - white card */
[data-testid="stSidebar"] button[kind="secondary"],
div.new-chat-card button {{
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    color: #1d1d1f !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin-bottom: 12px !important;
}}

/* ============================================================
   CHAT INPUT - Force white rounded pill
   ============================================================ */
[data-testid="stChatInput"] {{
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08) !important;
    padding: 4px 4px !important;
}}
[data-testid="stChatInput"] > div {{
    background: #ffffff !important;
    border-radius: 16px !important;
}}
[data-testid="stChatInput"] textarea {{
    background: #ffffff !important;
    color: #1d1d1f !important;
}}
/* The send button inside chat input */
[data-testid="stChatInput"] button {{
    background: #007aff !important;
    border-radius: 10px !important;
    color: #fff !important;
}}

/* Fix dark bottom bar on Streamlit Cloud */
[data-testid="stBottomBlockContainer"] {{
    background: #ffffff !important;
    border-top: 1px solid rgba(0,0,0,0.06) !important;
}}

/* ============================================================
   MODEL SELECTOR - Hide from main content, float top-right
   ============================================================ */
div.model-selector-float {{
    position: fixed !important;
    top: 18px !important;
    right: 40px !important;
    z-index: 10001 !important;
    width: 140px !important;
}}
div.model-selector-float [data-testid="stSelectbox"] > div > div {{
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    color: #1d1d1f !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}}

/* ============================================================
   HERO SECTION / LANDING
   ============================================================ */
.hero-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-top: 22vh;
    width: 100%;
}}
.hero-pill {{
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 20px;
    background: #ffffff; border: 1px solid rgba(0,0,0,0.08);
    border-radius: 40px;
    font-size: 0.72rem; font-weight: 800; text-transform: uppercase;
    color: #86868b; letter-spacing: 0.07em;
    margin-bottom: 2.5rem;
}}
.pill-dot {{ width: 6px; height: 6px; background: #007aff; border-radius: 50%; }}
.hero-title {{
    font-size: clamp(3.5rem, 9vw, 6rem);
    font-weight: 800; line-height: 1.04; letter-spacing: -0.05em;
    margin-bottom: 2rem;
}}
.hero-title span {{ color: #007aff; }}
.hero-sub {{
    font-size: 1.35rem; color: #86868b; max-width: 680px;
    font-weight: 500; line-height: 1.65; margin-bottom: 4rem;
}}

/* ============================================================
   LANDING + DASHBOARD BUTTONS Reset
   ============================================================ */
/* By default reset all buttons first */
button, .stButton button {{
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}

/* Primary (blue) button via wrapper */
div.btn-blue button {{
    background: #007aff !important;
    color: #ffffff !important;
    border-radius: 35px !important;
    padding: 14px 36px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    border: none !important;
    box-shadow: 0 12px 30px -6px rgba(0, 122, 255, 0.5) !important;
}}
div.btn-blue button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 40px -6px rgba(0, 122, 255, 0.55) !important;
}}

/* Secondary (white bordered) button via wrapper */
div.btn-white button {{
    background: #ffffff !important;
    color: #1d1d1f !important;
    border-radius: 35px !important;
    padding: 14px 36px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    border: 1.5px solid rgba(0,0,0,0.12) !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
}}

/* Header go-to-app */
div.btn-text button {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #1d1d1f !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0 !important;
}}

/* Disclaimer */
.disclaimer {{
    position: fixed; bottom: 18px;
    left: 0; right: 0; text-align: center;
    font-size: 0.72rem; color: #86868b;
    pointer-events: none;
}}

/* AI icon bubble */
.ai-row {{ display: flex; align-items: flex-start; gap: 14px; margin-bottom: 2rem; }}
.ai-ic {{
    width: 32px; height: 32px; flex-shrink: 0;
    background: rgba(0,122,255,0.08); color: #007aff;
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}}

/* chat message bubbles fix */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    box-shadow: none !important;
}}

</style>
""", unsafe_allow_html=True)

# =========================================================================
# LANDING PAGE
# =========================================================================
if st.session_state.active_view == "landing":
    # Fixed header
    st.markdown("""
    <div style="position:fixed;top:0;left:0;right:0;height:72px;display:flex;
    justify-content:space-between;align-items:center;padding:0 6%;z-index:10000;
    background:rgba(255,255,255,0.85);backdrop-filter:blur(20px);
    border-bottom:1px solid rgba(0,0,0,0.06);">
        <div style="display:flex;align-items:center;gap:12px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span style="font-weight:800;font-size:1.6rem;letter-spacing:-0.03em;">Sarwar AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Go to App header button
    _, hcol = st.columns([10, 1.5])
    with hcol:
        st.markdown('<div class="btn-text" style="position:fixed;top:22px;right:6%;z-index:10001;">', unsafe_allow_html=True)
        if st.button("Go to App", key="hdr_goto"):
            start_app()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-pill"><div class="pill-dot"></div>EVERYTHING IS BETTER IN ONE PLACE</div>
        <h1 class="hero-title">One interface for<br><span>multiple AI models.</span></h1>
        <p class="hero-sub">Experience the world's most capable models in a premium, calm, and intuitive workspace designed by humans for thinkers.</p>
    </div>
    """, unsafe_allow_html=True)

    # Hero buttons
    _, c2, _, c4, _ = st.columns([2.2, 1, 0.15, 1, 2.2])
    with c2:
        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        if st.button("Start Chatting", key="land_start"):
            start_app()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="btn-white">', unsafe_allow_html=True)
        if st.button("Explore Tools", key="land_tools"):
            st.session_state.active_view = "summarizer"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # N Avatar
    st.markdown('<div style="position:fixed;bottom:28px;left:28px;"><div style="width:38px;height:38px;background:#1d1d1f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.9rem;font-weight:800;box-shadow:0 6px 18px rgba(0,0,0,0.15);">N</div></div>', unsafe_allow_html=True)


# =========================================================================
# DASHBOARD
# =========================================================================
else:
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;padding:0 5px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span style="font-weight:700;font-size:1.15rem;color:#1d1d1f;">Sarwar AI</span>
        </div>
        """, unsafe_allow_html=True)

        # New Chat - white card style
        st.markdown('<div class="new-chat-card">', unsafe_allow_html=True)
        if st.button("＋  New Chat", key="nchat_btn", use_container_width=True):
            new_chat()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<p style='font-size:0.72rem;font-weight:800;color:#86868b;text-transform:uppercase;margin:1.5rem 0 0.6rem 10px;letter-spacing:0.06em;'>Menu</p>", unsafe_allow_html=True)

        def g(label, target, icon):
            active = st.session_state.active_view == target
            if active:
                # Inject one-time CSS to make THIS specific button blue
                st.markdown(f"""
                <style>
                button[data-testid="baseButton-secondary"][key="n_{target}"] {{
                    background: rgba(0,122,255,0.08) !important;
                    color: #007aff !important;
                    font-weight: 600 !important;
                }}
                </style>
                """, unsafe_allow_html=True)
            clicked = st.button(f"{icon}  {label}", key=f"n_{target}", use_container_width=True)
            if clicked:
                st.session_state.active_view = target
                st.rerun()

        g("Chat", "chat", "💬")
        g("Summarizer", "summarizer", "📝")
        g("Email Generator", "email", "✉️")
        g("Rewriter", "rewriter", "🔄")
        g("Content Gen", "content", "🎨")

        # Settings footer
        st.markdown("""
        <div style="position:absolute;bottom:28px;left:20px;right:20px;display:flex;align-items:center;gap:12px;padding:10px;">
            <div style="width:30px;height:30px;background:#1d1d1f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:800;">N</div>
            <span style="font-size:0.9rem;font-weight:600;color:#1d1d1f;">Settings</span>
        </div>
        """, unsafe_allow_html=True)

    # Main top bar
    view_name = "New Conversation" if st.session_state.active_view == "chat" else st.session_state.active_view.title()
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:1.4rem 2.5rem;border-bottom:1px solid rgba(0,0,0,0.06);margin-bottom:2.5rem;">
        <div style="color:#007aff;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>
        </div>
        <span style="font-weight:700;font-size:1.05rem;">{view_name}</span>
    </div>
    """, unsafe_allow_html=True)

    # Model selector - floated top right using a styled div
    st.markdown('<div class="model-selector-float">', unsafe_allow_html=True)
    sel_mod = st.selectbox("", get_available_models(), key="msel", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Chat view ──
    if st.session_state.active_view == "chat":
        if not st.session_state.current_session_id:
            new_chat()
        sid = st.session_state.current_session_id
        session = st.session_state.sessions[sid]

        if not session["messages"]:
            st.markdown('<div class="ai-row"><div class="ai-ic">✦</div><div style="padding-top:4px;font-weight:500;">Hello! I\'m Sarwar AI. How can I assist you today?</div></div>', unsafe_allow_html=True)

        for m in session["messages"]:
            with st.chat_message(m["role"]):
                if m["role"] == "assistant":
                    st.markdown(f'<div class="ai-row"><div class="ai-ic">✦</div><div style="flex:1;">{m["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.write(m["content"])

        if p := st.chat_input("Message Sarwar AI..."):
            session["messages"].append({"role": "user", "content": p})
            with st.chat_message("user"):
                st.write(p)
            with st.chat_message("assistant"):
                with st.spinner(""):
                    r = handle_chat(p, sel_mod, history=session["messages"][:-1])
                    st.markdown(f'<div class="ai-row"><div class="ai-ic">✦</div><div style="flex:1;">{r}</div></div>', unsafe_allow_html=True)
                    session["messages"].append({"role": "assistant", "content": r})
            st.rerun()

        st.markdown('<div class="disclaimer">Sarwar AI can make mistakes. Verify important information.</div>', unsafe_allow_html=True)

    # ── Summarizer ──
    elif st.session_state.active_view == "summarizer":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1rem 0;'><h1 style='font-size:2.8rem;font-weight:800;letter-spacing:-0.03em;margin-bottom:0.5rem;'>Text Summarizer</h1><p style='color:#86868b;font-size:1.1rem;margin-bottom:3rem;'>Distill complex documents into clear, actionable insights.</p>", unsafe_allow_html=True)
        text = st.text_area("Input Text", height=260, placeholder="Paste your text here...")
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Generate Summary", key="sum_btn"):
            if text:
                with st.spinner("Synthesizing..."):
                    res = run_summarizer(text, sel_mod)
                    st.markdown(f'<div style="background:#fbfbfd;border:1px solid rgba(0,0,0,0.06);padding:2.5rem;border-radius:24px;margin-top:2rem;line-height:1.7;">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Email ──
    elif st.session_state.active_view == "email":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1rem 0;'><h1 style='font-size:2.8rem;font-weight:800;letter-spacing:-0.03em;margin-bottom:0.5rem;'>Email Generator</h1><p style='color:#86868b;font-size:1.1rem;margin-bottom:3rem;'>Draft professional emails in any tone, instantly.</p>", unsafe_allow_html=True)
        ctx = st.text_area("Context", height=160, placeholder="What should the email be about?")
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Formal"])
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Draft Email", key="email_btn"):
            if ctx:
                with st.spinner("Drafting..."):
                    res = run_email_generator(ctx, tone.lower(), sel_mod)
                    st.markdown(f'<div style="background:#fbfbfd;border:1px solid rgba(0,0,0,0.06);padding:2.5rem;border-radius:24px;margin-top:2rem;line-height:1.7;">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Rewriter ──
    elif st.session_state.active_view == "rewriter":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1rem 0;'><h1 style='font-size:2.8rem;font-weight:800;letter-spacing:-0.03em;margin-bottom:0.5rem;'>Content Rewriter</h1><p style='color:#86868b;font-size:1.1rem;margin-bottom:3rem;'>Refine your writing while preserving its core meaning.</p>", unsafe_allow_html=True)
        text = st.text_area("Original Text", height=200, placeholder="Paste text to rewrite...")
        style = st.selectbox("Style", ["Academic", "Witty", "Direct", "Creative"])
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Rewrite Content", key="rw_btn"):
            if text:
                with st.spinner("Polishing..."):
                    res = run_rewriter(text, style.lower(), sel_mod)
                    st.markdown(f'<div style="background:#fbfbfd;border:1px solid rgba(0,0,0,0.06);padding:2.5rem;border-radius:24px;margin-top:2rem;">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Content Gen ──
    elif st.session_state.active_view == "content":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1rem 0;'><h1 style='font-size:2.8rem;font-weight:800;letter-spacing:-0.03em;margin-bottom:0.5rem;'>Content Creator</h1><p style='color:#86868b;font-size:1.1rem;margin-bottom:3rem;'>Generate high-quality social and web content instantly.</p>", unsafe_allow_html=True)
        topic = st.text_input("Topic", placeholder="e.g. The future of AI in healthcare")
        ctype = st.selectbox("Format", ["Blog Post", "LinkedIn Post", "Twitter Thread"])
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Create Content", key="cont_btn"):
            if topic:
                with st.spinner("Authoring..."):
                    res = run_content_generator(topic, ctype.lower(), sel_mod)
                    st.markdown(f'<div style="background:#fbfbfd;border:1px solid rgba(0,0,0,0.06);padding:2.5rem;border-radius:24px;margin-top:2rem;">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

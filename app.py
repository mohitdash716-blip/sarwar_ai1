"""
Sarwar AI — Premium Aesthetic Version
Smooth transitions, micro-animations, glassmorphism, and a refined Apple aesthetic.
"""

import uuid
import streamlit as st
from dotenv import load_dotenv
from utils.chat_handler import handle_chat, get_available_models
from utils.tools import run_summarizer, run_email_generator, run_rewriter, run_content_generator

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
    st.session_state.sessions[sid] = {"messages": []}
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"

def start_app():
    if not st.session_state.current_session_id:
        new_chat()
    st.session_state.active_view = "chat"

is_landing = st.session_state.active_view == "landing"

# ============================================================================
# GLOBAL CSS — Premium Aesthetic with Animations
# ============================================================================
st.markdown(f"""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── CSS Tokens ── */
:root {{
    --blue:   #007aff;
    --blue-glow: rgba(0, 122, 255, 0.35);
    --dark:   #1d1d1f;
    --muted:  #86868b;
    --light:  #f5f5f7;
    --border: rgba(0, 0, 0, 0.07);
    --glass:  rgba(255, 255, 255, 0.78);
    --shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
    --ease:   cubic-bezier(0.25, 1, 0.5, 1);
}}

/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; }}
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stHeader"], .main, section.main {{
    background: #ffffff !important;
    color: var(--dark) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}}

/* Clean Streamlit chrome */
#MainMenu, footer, header {{ visibility: hidden !important; display: none !important; }}
.stDeployButton, [data-testid="stDecoration"] {{ display: none !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}

/* ── LANDING: collapse sidebar ── */
{"""
section[data-testid="stSidebar"],
[data-testid="stSidebarNav"] {
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
}
""" if is_landing else ""}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
    background: rgba(251,251,253,0.9) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid var(--border) !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 1.5rem 1rem !important;
}}

/* Ghost all sidebar buttons */
section[data-testid="stSidebar"] button {{
    all: unset !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    padding: 10px 14px !important;
    margin: 2px 0 !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    cursor: pointer !important;
    transition: background 0.18s var(--ease), color 0.18s var(--ease) !important;
}}
section[data-testid="stSidebar"] button:hover {{
    background: rgba(0,0,0,0.04) !important;
    color: var(--dark) !important;
}}
/* Active nav via JS class name trick alternative */
div.snav-active button {{
    background: rgba(0, 122, 255, 0.09) !important;
    color: var(--blue) !important;
    font-weight: 600 !important;
}}

/* New Chat white card */
div.new-chat-wrap button {{
    all: unset !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    width: 100% !important;
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: var(--dark) !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    transition: box-shadow 0.2s var(--ease), transform 0.2s var(--ease) !important;
    margin: 1rem 0 !important;
}}
div.new-chat-wrap button:hover {{
    box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important;
    transform: translateY(-1px) !important;
}}

/* ── PRIMARY BUTTON ── */
div.btn-blue button {{
    all: unset !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: var(--blue) !important;
    color: #ffffff !important;
    padding: 15px 38px !important;
    border-radius: 40px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    cursor: pointer !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 14px 32px -6px var(--blue-glow) !important;
    transition: transform 0.22s var(--ease), box-shadow 0.22s var(--ease) !important;
}}
div.btn-blue button:hover {{
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 22px 40px -6px var(--blue-glow) !important;
}}
div.btn-blue button:active {{ transform: scale(0.98) !important; }}

/* ── SECONDARY BUTTON ── */
div.btn-white button {{
    all: unset !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #ffffff !important;
    color: var(--dark) !important;
    padding: 15px 38px !important;
    border-radius: 40px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    cursor: pointer !important;
    letter-spacing: -0.01em !important;
    border: 1.5px solid rgba(0,0,0,0.1) !important;
    transition: transform 0.22s var(--ease), border-color 0.22s var(--ease) !important;
}}
div.btn-white button:hover {{
    transform: translateY(-2px) !important;
    border-color: rgba(0,0,0,0.22) !important;
}}

/* ── GHOST TEXT BUTTON (header) ── */
div.btn-text button {{
    all: unset !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: var(--dark) !important;
    cursor: pointer !important;
    opacity: 0.8 !important;
    transition: opacity 0.2s !important;
}}
div.btn-text button:hover {{ opacity: 1 !important; }}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"],
[data-testid="stBottomBlockContainer"] {{
    background: #ffffff !important;
    border-color: var(--border) !important;
}}
[data-testid="stChatInput"] > div {{
    background: #ffffff !important;
    border-radius: 18px !important;
    border: 1px solid var(--border) !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.09) !important;
    transition: box-shadow 0.25s var(--ease) !important;
}}
[data-testid="stChatInput"] > div:focus-within {{
    box-shadow: 0 14px 50px rgba(0,122,255,0.15) !important;
    border-color: rgba(0,122,255,0.35) !important;
}}
[data-testid="stChatInput"] textarea {{
    background: transparent !important;
    color: var(--dark) !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stChatInput"] button {{
    background: var(--blue) !important;
    border-radius: 10px !important;
    color: #fff !important;
}}
[data-testid="stBottomBlockContainer"] {{
    background: #ffffff !important;
    border-top: 1px solid var(--border) !important;
}}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    box-shadow: none !important;
    animation: fadeSlideUp 0.35s var(--ease) forwards !important;
}}

/* ── MODEL SELECTOR FLOAT ── */
div.msel-float {{
    position: fixed !important;
    top: 20px !important;
    right: 40px !important;
    z-index: 10002 !important;
    width: 140px !important;
}}
div.msel-float [data-testid="stSelectbox"] > div > div {{
    background: var(--glass) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: var(--dark) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.07) !important;
    transition: box-shadow 0.2s var(--ease) !important;
}}

/* ── ANIMATIONS ── */
@keyframes fadeSlideUp {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}
@keyframes slideInLeft {{
    from {{ opacity: 0; transform: translateX(-20px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}

.hero-wrap {{ animation: fadeIn 0.7s var(--ease) forwards; }}
.sidebar-logo {{ animation: slideInLeft 0.4s var(--ease) forwards; }}

/* ── HERO ── */
.hero-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 22vh 2rem 4rem;
}}
.hero-pill {{
    display: inline-flex; align-items: center; gap: 9px;
    padding: 7px 20px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 40px;
    font-size: 0.72rem; font-weight: 800;
    color: var(--muted); text-transform: uppercase; letter-spacing: 0.07em;
    margin-bottom: 2.5rem;
    animation: fadeSlideUp 0.5s 0.1s var(--ease) both;
}}
.pill-dot {{ width: 7px; height: 7px; background: var(--blue); border-radius: 50%; }}

.hero-title {{
    font-size: clamp(3.5rem, 9vw, 6.2rem);
    font-weight: 900; line-height: 1.03; letter-spacing: -0.055em;
    margin-bottom: 2rem;
    animation: fadeSlideUp 0.55s 0.2s var(--ease) both;
}}
.hero-title span {{
    background: linear-gradient(135deg, #007aff 0%, #5ca0ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.hero-sub {{
    font-size: 1.3rem;
    color: var(--muted);
    max-width: 670px;
    line-height: 1.6;
    font-weight: 500;
    margin-bottom: 3.5rem;
    animation: fadeSlideUp 0.55s 0.3s var(--ease) both;
}}
.btns-row {{
    display: flex; gap: 16px; align-items: center;
    animation: fadeSlideUp 0.55s 0.4s var(--ease) both;
}}

/* Tool output cards */
.result-card {{
    background: #fbfbfd;
    border: 1px solid var(--border);
    padding: 2.5rem;
    border-radius: 24px;
    margin-top: 2rem;
    line-height: 1.75;
    animation: fadeSlideUp 0.4s var(--ease) forwards;
}}

/* AI Message Row */
.ai-row {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 1.5rem;
    animation: fadeSlideUp 0.35s var(--ease) forwards;
}}
.ai-ic {{
    width: 32px; height: 32px; flex-shrink: 0;
    background: rgba(0,122,255,0.09);
    color: var(--blue);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; font-weight: 600;
}}

/* Disclaimer */
.disclaimer {{
    position: fixed; bottom: 18px;
    left: 0; right: 0; text-align: center;
    font-size: 0.7rem; color: var(--muted);
    font-weight: 500; pointer-events: none;
    animation: fadeIn 0.5s 0.5s var(--ease) both;
}}

/* Tool headers */
.tool-title {{
    font-size: 2.8rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 0.5rem;
    animation: fadeSlideUp 0.4s var(--ease) forwards;
}}
.tool-sub {{
    color: var(--muted); font-size: 1.1rem; margin-bottom: 2.5rem;
    animation: fadeSlideUp 0.4s 0.1s var(--ease) both;
}}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# LANDING PAGE
# ============================================================================
if st.session_state.active_view == "landing":
    # Fixed glass header
    st.markdown("""
    <div style="position:fixed;top:0;left:0;right:0;height:72px;display:flex;
    justify-content:space-between;align-items:center;padding:0 6%;z-index:9999;
    background:var(--glass, rgba(255,255,255,0.8));
    backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
    border-bottom:1px solid rgba(0,0,0,0.06);
    animation: fadeIn 0.5s ease forwards;">
        <div style="display:flex;align-items:center;gap:12px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span style="font-weight:800;font-size:1.6rem;letter-spacing:-0.04em;color:#1d1d1f;">Sarwar AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Go to App button (native, floated)
    _, hc = st.columns([11, 1.5])
    with hc:
        st.markdown('<div class="btn-text" style="position:fixed;top:23px;right:6%;z-index:10000;">', unsafe_allow_html=True)
        if st.button("Go to App →", key="hdr_go"):
            start_app(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-pill"><div class="pill-dot"></div>EVERYTHING IS BETTER IN ONE PLACE</div>
        <h1 class="hero-title">One interface for<br><span>multiple AI models.</span></h1>
        <p class="hero-sub">Experience the world's most capable models in a premium, calm, and intuitive workspace designed by humans, for thinkers.</p>
    </div>
    """, unsafe_allow_html=True)

    # Buttons — centered via columns
    _, c2, _, c4, _ = st.columns([2.2, 1, 0.12, 1, 2.2])
    with c2:
        st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
        if st.button("Start Chatting", key="l_start"):
            start_app(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="btn-white">', unsafe_allow_html=True)
        if st.button("Explore Tools", key="l_tools"):
            st.session_state.active_view = "summarizer"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # N avatar bottom left
    st.markdown('<div style="position:fixed;bottom:28px;left:30px;"><div style="width:38px;height:38px;background:#1d1d1f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.88rem;font-weight:800;box-shadow:0 8px 22px rgba(0,0,0,0.15);transition:transform 0.2s ease;cursor:pointer;">N</div></div>', unsafe_allow_html=True)


# ============================================================================
# DASHBOARD / APP VIEWS
# ============================================================================
else:
    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo" style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;padding:0 6px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1-8.313-12.446z"/>
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span style="font-weight:700;font-size:1.15rem;color:#1d1d1f;letter-spacing:-0.02em;">Sarwar AI</span>
        </div>
        """, unsafe_allow_html=True)

        # New Chat Card
        st.markdown('<div class="new-chat-wrap">', unsafe_allow_html=True)
        if st.button("＋  New Chat", key="nc_btn", use_container_width=True):
            new_chat(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<p style='font-size:0.7rem;font-weight:800;color:#86868b;text-transform:uppercase;margin:1.5rem 0 0.7rem 10px;letter-spacing:0.08em;'>Menu</p>", unsafe_allow_html=True)

        def nav(label, tgt, icon):
            active = st.session_state.active_view == tgt
            cls = "snav-active" if active else ""
            st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{tgt}", use_container_width=True):
                st.session_state.active_view = tgt; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        nav("Chat", "chat", "💬")
        nav("Summarizer", "summarizer", "📝")
        nav("Email Generator", "email", "✉️")
        nav("Rewriter", "rewriter", "🔄")
        nav("Content Gen", "content", "🎨")

        st.markdown("""
        <div style="position:absolute;bottom:28px;left:20px;right:20px;display:flex;align-items:center;gap:12px;padding:10px;cursor:pointer;">
            <div style="width:30px;height:30px;background:#1d1d1f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:800;flex-shrink:0;">N</div>
            <span style="font-size:0.88rem;font-weight:600;color:#1d1d1f;">Settings</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Top Bar ───────────────────────────────────────────────────────────────
    view_nm = "New Conversation" if st.session_state.active_view == "chat" else st.session_state.active_view.title()
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:1.4rem 2.8rem;
    border-bottom:1px solid rgba(0,0,0,0.06);margin-bottom:2.5rem;
    animation:slideInLeft 0.4s cubic-bezier(0.25,1,0.5,1) forwards;">
        <div style="color:#007aff;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>
        </div>
        <span style="font-weight:700;font-size:1rem;color:#1d1d1f;">{view_nm}</span>
    </div>
    """, unsafe_allow_html=True)

    # Floating model selector
    st.markdown('<div class="msel-float">', unsafe_allow_html=True)
    sel_mod = st.selectbox("", get_available_models(), key="msl", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CHAT ─────────────────────────────────────────────────────────────────
    if st.session_state.active_view == "chat":
        if not st.session_state.current_session_id: new_chat()
        sid = st.session_state.current_session_id
        session = st.session_state.sessions[sid]

        if not session["messages"]:
            st.markdown('<div class="ai-row"><div class="ai-ic">✦</div><div style="padding-top:3px;font-weight:500;font-size:0.97rem;">Hello! I\'m Sarwar AI. How can I assist you today?</div></div>', unsafe_allow_html=True)

        for m in session["messages"]:
            with st.chat_message(m["role"]):
                if m["role"] == "assistant":
                    st.markdown(f'<div class="ai-row"><div class="ai-ic">✦</div><div style="flex:1;line-height:1.65;">{m["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.write(m["content"])

        if p := st.chat_input("Message Sarwar AI..."):
            session["messages"].append({"role": "user", "content": p})
            with st.chat_message("user"): st.write(p)
            with st.chat_message("assistant"):
                with st.spinner(""):
                    r = handle_chat(p, sel_mod, history=session["messages"][:-1])
                    st.markdown(f'<div class="ai-row"><div class="ai-ic">✦</div><div style="flex:1;line-height:1.65;">{r}</div></div>', unsafe_allow_html=True)
                    session["messages"].append({"role": "assistant", "content": r})
            st.rerun()

        st.markdown('<div class="disclaimer">Sarwar AI can make mistakes. Verify important information.</div>', unsafe_allow_html=True)

    # ── SUMMARIZER ───────────────────────────────────────────────────────────
    elif st.session_state.active_view == "summarizer":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='tool-title'>Text Summarizer</h1>", unsafe_allow_html=True)
        st.markdown("<p class='tool-sub'>Distill long documents into clear, actionable insights.</p>", unsafe_allow_html=True)
        text = st.text_area("", height=280, placeholder="Paste your text here...", label_visibility="collapsed")
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Generate Summary", key="s_btn"):
            if text:
                with st.spinner(""):
                    res = run_summarizer(text, sel_mod)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── EMAIL ────────────────────────────────────────────────────────────────
    elif st.session_state.active_view == "email":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='tool-title'>Email Generator</h1>", unsafe_allow_html=True)
        st.markdown("<p class='tool-sub'>Draft perfectly toned professional emails in seconds.</p>", unsafe_allow_html=True)
        ctx = st.text_area("", height=180, placeholder="What should the email be about?", label_visibility="collapsed")
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Formal"])
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Draft Email", key="e_btn"):
            if ctx:
                with st.spinner(""):
                    res = run_email_generator(ctx, tone.lower(), sel_mod)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── REWRITER ─────────────────────────────────────────────────────────────
    elif st.session_state.active_view == "rewriter":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='tool-title'>Content Rewriter</h1>", unsafe_allow_html=True)
        st.markdown("<p class='tool-sub'>Refine your writing into any style while preserving intent.</p>", unsafe_allow_html=True)
        text = st.text_area("", height=220, placeholder="Paste the text to rewrite...", label_visibility="collapsed")
        style = st.selectbox("Style", ["Academic", "Witty", "Direct", "Creative"])
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Rewrite", key="r_btn"):
            if text:
                with st.spinner(""):
                    res = run_rewriter(text, style.lower(), sel_mod)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── CONTENT GEN ──────────────────────────────────────────────────────────
    elif st.session_state.active_view == "content":
        st.markdown("<div style='max-width:820px;margin:0 auto;padding:1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='tool-title'>Content Creator</h1>", unsafe_allow_html=True)
        st.markdown("<p class='tool-sub'>Generate high-quality social and web content instantly.</p>", unsafe_allow_html=True)
        topic = st.text_input("", placeholder="e.g. The future of AI in everyday life", label_visibility="collapsed")
        ctype = st.selectbox("Format", ["Blog Post", "LinkedIn Post", "Twitter Thread"])
        st.markdown('<div class="btn-blue" style="width:fit-content;">', unsafe_allow_html=True)
        if st.button("Create Content", key="c_btn"):
            if topic:
                with st.spinner(""):
                    res = run_content_generator(topic, ctype.lower(), sel_mod)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

"""
Sarwar AI — Main Streamlit Application
A unified AI assistant platform with ChatGPT-style UI.
"""

import os
import uuid
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
    page_title="Sarwar AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Apple Inspired Minimalist Light Theme ── */

/* ── Root & global reset ── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    background-color: #f5f5f7;
    color: #1d1d1f;
    -webkit-font-smoothing: antialiased;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── App container ── */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 0, 0, 0.05);
    width: 260px !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1rem 0.75rem !important;
}

/* ── Sidebar logo area ── */
.sarwar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.5rem 0 1rem 0;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}
.sarwar-logo .logo-icon {
    font-size: 1.6rem;
    color: #007aff;
}
.sarwar-logo .logo-text {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1d1d1f;
    letter-spacing: -0.01em;
}

/* ── New Chat button ── */
.stButton > button {
    width: 100%;
    background: #ffffff;
    color: #007aff !important;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}
.stButton > button:hover {
    background: #fbfbfd;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

/* ── Section labels in sidebar ── */
.sidebar-section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #86868b;
    padding: 0.9rem 0 0.4rem 0.4rem;
}

/* ── History item ── */
.history-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.5rem 0.6rem;
    border-radius: 10px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    color: #515154;
    transition: all 0.15s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 2px;
    border: 1px solid transparent;
}
.history-item:hover {
    background: rgba(0,0,0,0.03);
    color: #1d1d1f;
}
.history-item.active {
    background: #ffffff;
    color: #007aff;
    border: 1px solid rgba(0,0,0,0.04);
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

/* ── API Status badges ── */
.api-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    color: #86868b;
    padding: 2px 0 2px 0.4rem;
}
.api-dot-ok  { color: #34c759; }
.api-dot-err { color: #ff3b30; }

/* ── Model selector ── */
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 10px !important;
    color: #1d1d1f !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
[data-testid="stSelectbox"] label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #86868b !important;
    padding-left: 0.4rem;
}

/* ── Main chat area ── */
.chat-header {
    padding: 1.2rem 2rem 0.5rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #1d1d1f;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    background: rgba(245, 245, 247, 0.8);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 10;
}
.model-badge {
    display: inline-block;
    background: #ffffff;
    color: #007aff;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 2px 10px;
    margin-left: 8px;
    letter-spacing: 0.02em;
}

/* ── Chat messages ── */
.chat-viewport {
    padding: 1rem 2rem 7rem 2rem;
    min-height: 60vh;
}

/* User message bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #007aff !important;
    color: #ffffff !important;
    border-radius: 18px 18px 4px 18px !important;
    border: none !important;
    margin: 0.5rem 0 0.5rem 20% !important;
    padding: 0.9rem 1.2rem !important;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
}

/* Assistant message bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: #ffffff !important;
    color: #1d1d1f !important;
    border-radius: 18px 18px 18px 4px !important;
    border: 1px solid rgba(0,0,0,0.04) !important;
    margin: 0.5rem 20% 0.5rem 0 !important;
    padding: 0.9rem 1.2rem !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
}

/* Avatar circles */
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"] {
    background-color: transparent !important;
}

/* ── Chat input bar ── */
[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 24px !important;
    padding: 4px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #1d1d1f !important;
    font-size: 1rem !important;
    padding-left: 8px !important;
}
[data-testid="stChatInput"] button {
    background: #007aff !important;
    border-radius: 50% !important;
    color: white !important;
    padding: 4px !important;
}

/* ── Tool page ── */
.tool-header {
    padding: 1.5rem 2rem 0.5rem 2rem;
}
.tool-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1d1d1f;
    letter-spacing: -0.02em;
}
.tool-subtitle {
    font-size: 0.9rem;
    color: #86868b;
    margin-top: 4px;
}

[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 14px !important;
    color: #1d1d1f !important;
    font-size: 0.95rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}
[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 12px !important;
    color: #1d1d1f !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}
[data-testid="stSelectbox"] select,
div[data-baseweb="select"] {
    background: #ffffff !important;
}

/* Output box */
.output-box {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 16px;
    padding: 1.4rem;
    color: #1d1d1f;
    font-size: 0.95rem;
    line-height: 1.6;
    white-space: pre-wrap;
    margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}

/* tool nav button – active state */
.tool-nav-active {
    background: #ffffff !important;
    color: #007aff !important;
    border-color: rgba(0,0,0,0.04) !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02) !important;
    font-weight: 600 !important;
}

/* Spinner */
[data-testid="stSpinner"] > div {
    border-top-color: #007aff !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 6px; }

/* Remove Streamlit padding from columns */
.element-container { margin: 0 !important; }

/* Welcome screen */
.welcome-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    text-align: center;
}
.welcome-icon {
    font-size: 4rem;
    margin-bottom: 0.5rem;
}
.welcome-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1d1d1f;
    margin-bottom: 0.5rem;
    letter-spacing: -0.03em;
}
.welcome-sub {
    font-size: 1rem;
    color: #86868b;
    max-width: 440px;
    line-height: 1.5;
}
.suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 2.5rem;
    max-width: 540px;
}
.suggestion-card {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: #515154;
    text-align: left;
    cursor: default;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.suggestion-card:hover { 
    border-color: rgba(0,0,0,0.1); 
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    transform: translateY(-2px);
}
.suggestion-card strong { 
    display: block; 
    color: #1d1d1f; 
    margin-bottom: 4px; 
    font-size: 0.9rem; 
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Session state initialisation ──────────────────────────────────────────────
def init_session_state():
    """Initialise all required session state keys."""
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}         # {session_id: {"title": str, "messages": list}}
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None
    if "active_view" not in st.session_state:
        st.session_state.active_view = "chat"  # "chat" | "summarizer" | "email" | "rewriter" | "content"
    if "tool_output" not in st.session_state:
        st.session_state.tool_output = {}


init_session_state()


# ── Helpers ───────────────────────────────────────────────────────────────────
def new_chat():
    """Create a new empty chat session and switch to it."""
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().strftime("%H:%M"),
    }
    st.session_state.current_session_id = sid
    st.session_state.active_view = "chat"


def get_current_messages() -> list:
    sid = st.session_state.current_session_id
    if sid and sid in st.session_state.sessions:
        return st.session_state.sessions[sid]["messages"]
    return []


def add_message(role: str, content: str):
    sid = st.session_state.current_session_id
    if sid and sid in st.session_state.sessions:
        st.session_state.sessions[sid]["messages"].append({"role": role, "content": content})
        # Auto-title from first user message
        msgs = st.session_state.sessions[sid]["messages"]
        user_msgs = [m for m in msgs if m["role"] == "user"]
        if len(user_msgs) == 1:
            first = user_msgs[0]["content"]
            st.session_state.sessions[sid]["title"] = first[:40] + ("…" if len(first) > 40 else "")


def check_api_status() -> dict:
    return {
        "OpenAI":    bool(os.environ.get("OPENAI_API_KEY")),
        "Anthropic": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "Google":    bool(os.environ.get("GOOGLE_API_KEY")),
    }


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sarwar-logo">
      <span class="logo-icon">✦</span>
      <span class="logo-text">Sarwar AI</span>
    </div>
    """, unsafe_allow_html=True)

    # New Chat button
    if st.button("＋  New Chat", key="new_chat_btn"):
        new_chat()
        st.rerun()

    # Model selector
    st.markdown('<div class="sidebar-section-label">Model</div>', unsafe_allow_html=True)
    selected_model = st.selectbox(
        "Model",
        get_available_models(),
        label_visibility="collapsed",
        key="selected_model",
    )

    # Chat History
    st.markdown('<div class="sidebar-section-label">Chat history</div>', unsafe_allow_html=True)

    sessions = st.session_state.sessions
    if sessions:
        # Show most recent first
        sorted_sessions = sorted(sessions.items(), key=lambda x: x[1]["created_at"], reverse=True)
        for sid, meta in sorted_sessions:
            is_active = sid == st.session_state.current_session_id
            css_class = "history-item active" if is_active else "history-item"
            icon = "💬" if is_active else "🗨️"
            label = meta["title"]
            # Use a button per history item (styled as text)
            if st.button(f"{icon}  {label}", key=f"hist_{sid}", use_container_width=True):
                st.session_state.current_session_id = sid
                st.session_state.active_view = "chat"
                st.rerun()
    else:
        st.markdown('<div style="font-size:0.78rem;color:#444;padding:6px 0;">No conversations yet.</div>', unsafe_allow_html=True)

    # AI Tools navigation
    st.markdown('<div class="sidebar-section-label">AI Tools</div>', unsafe_allow_html=True)

    tool_items = [
        ("📝", "summarizer",  "Summarizer"),
        ("✉️", "email",       "Email Generator"),
        ("🔄", "rewriter",    "Rewriter"),
        ("🎨", "content",     "Content Generator"),
    ]
    for icon, key, label in tool_items:
        is_active = st.session_state.active_view == key
        btn_label = f"{icon}  {label}"
        if st.button(btn_label, key=f"tool_nav_{key}", use_container_width=True):
            st.session_state.active_view = key
            st.rerun()

    # API Key status
    st.markdown('<div class="sidebar-section-label">API Status</div>', unsafe_allow_html=True)
    status = check_api_status()
    for provider, ok in status.items():
        dot_class = "api-dot-ok" if ok else "api-dot-err"
        dot = "●" if ok else "●"
        txt = "Connected" if ok else "Key missing"
        st.markdown(
            f'<div class="api-status"><span class="{dot_class}">{dot}</span>{provider}: {txt}</div>',
            unsafe_allow_html=True
        )


# ── Main area ─────────────────────────────────────────────────────────────────
view = st.session_state.active_view

# ─────────────────────── CHAT VIEW ───────────────────────────────────────────
if view == "chat":
    # Ensure there's an active session
    if st.session_state.current_session_id is None:
        new_chat()

    messages = get_current_messages()

    # Header bar
    st.markdown(
        f'<div class="chat-header">Sarwar AI '
        f'<span class="model-badge">{selected_model}</span></div>',
        unsafe_allow_html=True,
    )

    # Chat viewport
    st.markdown('<div class="chat-viewport">', unsafe_allow_html=True)

    if not messages:
        # Welcome / empty state
        st.markdown("""
        <div class="welcome-wrap">
            <div class="welcome-icon">✨</div>
            <div class="welcome-title">Sarwar AI</div>
            <div class="welcome-sub">
                Your unified AI assistant. Ask anything — from coding and writing
                to research and brainstorming.
            </div>
            <div class="suggestion-grid">
                <div class="suggestion-card"><strong>✍️ Write</strong>Draft a cover letter for a software engineer role</div>
                <div class="suggestion-card"><strong>💡 Explain</strong>How does quantum entanglement work?</div>
                <div class="suggestion-card"><strong>🧑‍💻 Code</strong>Write a Python function to parse JSON safely</div>
                <div class="suggestion-card"><strong>📊 Analyse</strong>What are the pros and cons of microservices?</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in messages:
            with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "✨"):
                st.markdown(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

    # Input bar (sticky at bottom via Streamlit's native chat_input)
    if prompt := st.chat_input("Message Sarwar AI…"):
        add_message("user", prompt)
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Thinking…"):
                reply = handle_chat(
                    prompt=prompt,
                    selected_model=selected_model,
                    history=get_current_messages()[:-1],  # exclude the just-added user message
                )
            st.markdown(reply)
        add_message("assistant", reply)
        st.rerun()


# ─────────────────────── TOOL VIEWS ──────────────────────────────────────────
elif view in ("summarizer", "email", "rewriter", "content"):

    TOOL_META = {
        "summarizer": {
            "title": "📝 Text Summarizer",
            "subtitle": "Paste any text and get a clear, concise summary.",
        },
        "email": {
            "title": "✉️ Email Generator",
            "subtitle": "Describe your email context and get a polished draft.",
        },
        "rewriter": {
            "title": "🔄 Text Rewriter",
            "subtitle": "Transform your text into a different style or tone.",
        },
        "content": {
            "title": "🎨 Content Generator",
            "subtitle": "Generate engaging content for any topic.",
        },
    }

    meta = TOOL_META[view]
    st.markdown(
        f'<div class="tool-header">'
        f'<div class="tool-title">{meta["title"]}</div>'
        f'<div class="tool-subtitle">{meta["subtitle"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    output_key = f"tool_output_{view}"
    if output_key not in st.session_state:
        st.session_state[output_key] = ""

    with st.container():
        col, _ = st.columns([3, 1])
        with col:
            # ── Summarizer ──
            if view == "summarizer":
                input_text = st.text_area(
                    "Text to summarize",
                    placeholder="Paste your article, document, or notes here…",
                    height=200,
                    key="summarizer_input",
                )
                if st.button("✨ Summarize", key="summarizer_btn"):
                    if input_text.strip():
                        with st.spinner("Summarizing…"):
                            out = run_summarizer(input_text, selected_model)
                        st.session_state[output_key] = out
                    else:
                        st.warning("Please enter some text to summarize.")

            # ── Email Generator ──
            elif view == "email":
                context = st.text_area(
                    "Email context",
                    placeholder="e.g. Write a follow-up email to a client after a product demo…",
                    height=130,
                    key="email_context",
                )
                tone = st.selectbox(
                    "Tone",
                    ["Professional", "Friendly", "Formal", "Casual", "Persuasive"],
                    key="email_tone",
                )
                if st.button("✉️ Generate Email", key="email_btn"):
                    if context.strip():
                        with st.spinner("Drafting your email…"):
                            out = run_email_generator(context, tone.lower(), selected_model)
                        st.session_state[output_key] = out
                    else:
                        st.warning("Please describe what the email should be about.")

            # ── Rewriter ──
            elif view == "rewriter":
                input_text = st.text_area(
                    "Text to rewrite",
                    placeholder="Paste the text you want to rewrite…",
                    height=180,
                    key="rewriter_input",
                )
                style = st.selectbox(
                    "Rewriting style",
                    ["Formal", "Casual", "Simpler", "More Detailed", "Persuasive", "Academic"],
                    key="rewriter_style",
                )
                if st.button("🔄 Rewrite", key="rewriter_btn"):
                    if input_text.strip():
                        with st.spinner("Rewriting…"):
                            out = run_rewriter(input_text, style.lower(), selected_model)
                        st.session_state[output_key] = out
                    else:
                        st.warning("Please enter some text to rewrite.")

            # ── Content Generator ──
            elif view == "content":
                topic = st.text_input(
                    "Topic",
                    placeholder="e.g. The future of renewable energy",
                    key="content_topic",
                )
                content_type = st.selectbox(
                    "Content type",
                    ["Blog Post", "Social Media Caption", "Product Description",
                     "LinkedIn Post", "Twitter Thread", "YouTube Script", "Press Release"],
                    key="content_type",
                )
                if st.button("🎨 Generate Content", key="content_btn"):
                    if topic.strip():
                        with st.spinner("Generating content…"):
                            out = run_content_generator(topic, content_type, selected_model)
                        st.session_state[output_key] = out
                    else:
                        st.warning("Please enter a topic.")

            # ── Output ──
            if st.session_state.get(output_key):
                st.markdown("**Output:**")
                st.markdown(
                    f'<div class="output-box">{st.session_state[output_key]}</div>',
                    unsafe_allow_html=True,
                )
                st.download_button(
                    "⬇️ Download",
                    data=st.session_state[output_key],
                    file_name=f"sarwar_ai_{view}_output.txt",
                    mime="text/plain",
                    key=f"download_{view}",
                )

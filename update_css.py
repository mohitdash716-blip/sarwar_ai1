import re

with open("c:\\Users\\mohit\\OneDrive\\Desktop\\sarwar ai\\app.py", "r", encoding="utf-8") as f:
    content = f.read()

new_css = """<style>
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
</style>"""

content = re.sub(r'<style>.*?</style>', new_css, content, flags=re.DOTALL)

# Let's also remove the previous gradient icon styling for the welcome screen in the python string
content = content.replace('<div class="welcome-icon">✦</div>', '<div class="welcome-icon">✨</div>')

with open("c:\\Users\\mohit\\OneDrive\\Desktop\\sarwar ai\\app.py", "w", encoding="utf-8") as f:
    f.write(content)

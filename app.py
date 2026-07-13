import streamlit as st
import time
from sentiment import get_sentiment
from chatbot import get_response
from data_manager import (
    get_user_conversations,
    save_user_conversations,
    user_exists,
    verify_password,
    register_user
)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Synapse AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CSS ----------
st.markdown("""
<style>
    /* ---------- GLOBAL ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
    .stApp { background: #0b0e17; }
    .main > div { background: transparent !important; padding: 0 !important; margin: 0 !important; box-shadow: none !important; border: none !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* DO NOT hide the header */
    header {
        background: transparent !important;
    }

    /* ---------- TOP NAV ---------- */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 30px;
        background: rgba(20, 25, 40, 0.8);
        backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        height: 64px;
    }
    .top-nav .logo {
        font-size: 1.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .top-nav .nav-right { display: flex; align-items: center; gap: 20px; }
    .top-nav .nav-right .avatar {
        width: 36px; height: 36px; border-radius: 50%;
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        display: flex; align-items: center; justify-content: center;
        font-weight: 600; color: white; font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    .top-nav .nav-right .status-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #10b981; display: inline-block; margin-left: 4px;
    }

    header[data-testid="stHeader"]{
        z-index:1101 !important;
        background:transparent !important;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"]{
        background:#0f1424 !important;
        overflow-y:auto !important;
        height:100vh !important;

        width:330px !important;
        min-width:330px !important;
        max-width:330px !important;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar{
        width:8px;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar-track{
        background:#151a2d;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb{
        background:#7c3aed;
        border-radius:10px;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover{
        background:#9f67ff;
    }
    .sidebar .user-info {
        padding: 12px 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 16px;
    }
    .sidebar .user-info .user-avatar {
        width: 40px; height: 40px; border-radius: 50%;
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; color: white; font-size: 1rem;
    }
    .sidebar .user-info .user-name { color: white; font-weight: 600; font-size: 0.95rem; }
    .sidebar .user-info .user-status { color: rgba(255,255,255,0.3); font-size: 0.7rem; }
    .sidebar .nav-item {
        display: flex; align-items: center; gap: 12px;
        padding: 10px 14px; border-radius: 12px;
        color: rgba(255,255,255,0.5); font-weight: 500; font-size: 0.9rem;
        transition: 0.2s; cursor: pointer; margin-bottom: 2px;
    }
    .sidebar .nav-item:hover { background: rgba(255,255,255,0.05); color: white; }
    .sidebar .nav-item.active { background: rgba(124, 58, 237, 0.15); color: #a78bfa; border: 1px solid rgba(124, 58, 237, 0.2); }
    .sidebar .nav-item .icon { font-size: 1.2rem; width: 24px; text-align: center; }
    .sidebar .nav-divider { height: 1px; background: rgba(255,255,255,0.05); margin: 12px 0; }
    .sidebar .section-label {
        font-size: 0.65rem; text-transform: uppercase;
        color: rgba(255,255,255,0.2); letter-spacing: 1px;
        padding: 8px 14px; margin-top: 6px;
    }
    /* Sidebar buttons - Streamlit overrides */
    .sidebar .stButton button {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.06);
        color: white;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 500;
        width: 100%;
        text-align: left;
        transition: 0.2s;
    }
    .sidebar .stButton button:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(124, 58, 237, 0.3);
    }

    /* ---------- MAIN CONTENT ---------- */
    .main-content .page-title{
        color:#ffffff !important;
        font-size:30px;
        font-weight:700;
    }

    /* ---------- CARDS ---------- */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 16px;
        margin-bottom: 25px;
    }
    .stat-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 16px 20px;
        transition: 0.3s;
    }
    .stat-card:hover { border-color: rgba(124, 58, 237, 0.2); background: rgba(255,255,255,0.05); }
    .stat-card .stat-label { font-size: 0.75rem; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.5px; }
    .stat-card .stat-value { font-size: 1.8rem; font-weight: 700; color: white; margin-top: 2px; }
    .stat-card .stat-icon { font-size: 1.5rem; float: right; opacity: 0.3; }

    /* ---------- CHAT PANEL ---------- */
    .chat-panel {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 20px;
    }
    .chat-container {
        flex: 1;
        overflow-y: auto;
        padding: 10px 10px 20px 10px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .chat-container::-webkit-scrollbar { width: 4px; }
    .chat-container::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); border-radius: 10px; }
    .chat-container::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #a78bfa, #7c3aed); border-radius: 10px; }


    .user-message{
        background:linear-gradient(135deg,#7c3aed,#6d28d9);
        color:white;
        padding:12px 18px;
        border-radius:18px 18px 5px 18px;
        width:fit-content;
        max-width:65%;
        margin:12px 40px 12px auto;
    }

    .assistant-message{
        background:#1c2232;
        color:white;
        padding:12px 18px;
        border-radius:18px 18px 18px 5px;
        width:fit-content;
        max-width:65%;
        margin:12px 0 12px 40px;
    }

    .sentiment-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.65rem;
        margin-top: 4px;
        text-transform: uppercase;
    }
    .positive { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.1); }
    .negative { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.1); }
    .neutral { background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.1); }

    /* Chat input */
    .stChatInput > div > div > textarea {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 10px 18px !important;
        font-size: 0.95rem;
    }
    .stChatInput > div > div > textarea:focus {
        border-color: #7c3aed !important;
        background: rgba(255,255,255,0.05) !important;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.05);
    }

    /* ---------- AUTH PAGE ---------- */
    .auth-page {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: radial-gradient(circle at 20% 30%, #0b0e17, #0f172a);
        padding: 20px;
    }
    .auth-container {
        display: flex;
        flex-wrap: wrap;
        max-width: 960px;
        width: 100%;
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(20px);
        border-radius: 40px;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 30px 80px rgba(0,0,0,0.5);
        overflow: hidden;
    }
    .auth-brand {
        flex: 1 1 280px;
        padding: 40px 35px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: rgba(124, 58, 237, 0.05);
        border-right: 1px solid rgba(255,255,255,0.04);
    }
    .auth-brand .brand-logo {
        font-size: 2rem; font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .auth-brand .brand-tagline {
        color: rgba(255,255,255,0.7);
        font-size: 1rem;
        font-weight: 300;
        line-height: 1.6;
    }
    .auth-brand .brand-features { margin-top: 25px; display: flex; flex-direction: column; gap: 10px; }
    .auth-brand .brand-features .feature {
        display: flex; align-items: center; gap: 12px;
        color: rgba(255,255,255,0.5); font-size: 0.9rem;
    }
    .auth-form {
        flex: 1 1 280px;
        padding: 40px 35px;
    }
    .auth-form h2 {
        color: white; font-weight: 600; font-size: 1.6rem;
        margin-bottom: 4px; letter-spacing: -0.5px;
    }
    .auth-form .subtitle {
        color: rgba(255,255,255,0.4);
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    .auth-form .stTextInput > div > div > input {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        color: white;
        border-radius: 30px;
        padding: 10px 16px;
        margin: 4px 0;
        width: 100%;
    }
    .auth-form .stTextInput > div > div > input:focus {
        border-color: #7c3aed;
        background: rgba(255,255,255,0.06);
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);
    }
    .auth-form .stButton button {
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        border: none;
        border-radius: 30px;
        padding: 10px;
        color: white;
        font-weight: 600;
        width: 100%;
        margin-top: 8px;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    .auth-form .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.4);
    }
    .auth-form .switch-link {
        color: rgba(255,255,255,0.4);
        font-size: 0.85rem;
        margin-top: 12px;
        display: inline-block;
        cursor: pointer;
        transition: 0.3s;
        background: none;
        border: none;
        text-decoration: underline;
        text-underline-offset: 3px;
        text-decoration-color: rgba(255,255,255,0.1);
    }
    .auth-form .switch-link:hover { color: white; text-decoration-color: white; }
    .auth-form .back-link {
        color: rgba(255,255,255,0.3);
        font-size: 0.85rem;
        cursor: pointer;
        transition: 0.3s;
        background: none;
        border: none;
        text-decoration: none;
        display: inline-block;
        margin-bottom: 8px;
    }
    .auth-form .back-link:hover { color: white; }
    .auth-form .stAlert {
        background: rgba(255,0,0,0.05);
        border: none;
        border-radius: 20px;
        color: white;
        padding: 6px 14px;
    }

    /* ---------- LANDING ---------- */
    .landing-page {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        text-align: center;
        padding: 20px;
        background: radial-gradient(circle at 30% 20%, #0b0e17, #0f172a);
    }
    .landing-page .brand {
        font-size: 3rem; font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .landing-page .tagline {
        font-size: 1.6rem; font-weight: 300;
        color: rgba(255,255,255,0.7);
        margin-top: 6px;
    }
    .landing-page .desc {
        color: rgba(255,255,255,0.4);
        font-size: 1rem;
        margin: 16px 0 30px;
        line-height: 1.6;
        max-width: 550px;
    }
    .landing-page .stats {
        display: flex;
        justify-content: center;
        gap: 30px;
        flex-wrap: wrap;
        color: rgba(255,255,255,0.25);
        font-size: 0.85rem;
        margin-top: 40px;
    }

    /* Spinner */
    .stSpinner p{
        color:#ffffff !important;
        font-size:18px !important;
        font-weight:600 !important;
    }

    .stSpinner{
        color:#ffffff !important;
    }

    /* Sidebar expand/collapse button */


    /* Sidebar toggle icon */


    [data-testid="collapsedControl"]:hover {
        color: #a78bfa !important;
    }

    [data-testid="collapsedControl"]:hover svg {
        fill: #a78bfa !important;
        stroke: #a78bfa !important;
    }

    .stChatInput{
        position:fixed !important;
        left:400px !important;
        right:35px !important;
        bottom:10px !important;
        z-index:999;
    }

    .main .block-container{
        padding-bottom:120px !important;
    }

    .block-container{
        padding-left:100px !important;
        padding-right:30px !important;
        padding-top:90px !important;
        padding-bottom:120px !important;
    }

</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.conversations = []
    st.session_state.current_conv_id = None
    st.session_state.auth_mode = "login"
    st.session_state.page = "auth"

# ---------- FUNCTIONS ----------
def login_user(username):
    st.session_state.logged_in = True
    st.session_state.username = username
    convs = get_user_conversations(username)
    if not convs:
        conv_id = str(int(time.time()))
        convs = [{"id": conv_id, "name": "New Chat", "messages": []}]
        save_user_conversations(username, convs)
    st.session_state.conversations = convs
    # Create a new chat every login
    # Create a new chat only if the last chat is not already empty
    if (
        not st.session_state.conversations
        or st.session_state.conversations[-1]["messages"]
    ):
        conv_id = str(int(time.time()))

        new_conv = {
            "id": conv_id,
            "name": "New Chat",
            "messages": []
        }

        st.session_state.conversations.append(new_conv)

    st.session_state.current_conv_id = st.session_state.conversations[-1]["id"]

    save_user_conversations(
        username,
        st.session_state.conversations
    )

    st.session_state.page = "chat"

def logout_user():
    if st.session_state.username and st.session_state.conversations:
        save_user_conversations(st.session_state.username, st.session_state.conversations)
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.conversations = []
    st.session_state.current_conv_id = None
    st.session_state.page = "auth"
    st.rerun()

def auto_name_conversation(conv, first_message):
    if conv["name"] == "New Chat":
        name = first_message[:30] + ("..." if len(first_message) > 30 else "")
        conv["name"] = name
        save_user_conversations(st.session_state.username, st.session_state.conversations)

# ---------- AUTH PAGE ----------
def render_auth_page():

    left, center, right = st.columns([1, 1.2, 1])

    with center:

        st.markdown("""
        <div style="
        background:#161b2e;
        padding:40px;
        border-radius:20px;
        border:1px solid #2d3555;
        margin-top:80px;
        box-shadow:0 0 30px rgba(0,0,0,.3);
        ">

        <h1 style="text-align:center;color:white;">
        ⚡ Synapse AI
        </h1>

        <p style="text-align:center;color:#9aa4c7;margin-bottom:35px;">
        Sign in to continue
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Password"
            )

            if st.button("Login", use_container_width=True):

                if username and password:

                    if user_exists(username):

                        if verify_password(username,password):

                            login_user(username)
                            st.rerun()

                        else:
                            st.error("Incorrect password")

                    else:
                        st.error("User not found")

            st.markdown("---")

            if st.button(
                "Create New Account",
                use_container_width=True
            ):
                st.session_state.auth_mode="register"
                st.rerun()

        else:

            username = st.text_input(
                "Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password"
            )

            if st.button("Register",use_container_width=True):

                if password!=confirm:

                    st.error("Passwords don't match")

                elif user_exists(username):

                    st.error("User already exists")

                else:

                    register_user(username,password)

                    login_user(username)

                    st.rerun()

            st.markdown("---")

            if st.button(
                "Back to Login",
                use_container_width=True
            ):
                st.session_state.auth_mode="login"
                st.rerun()

        st.markdown("</div>",unsafe_allow_html=True)


# ---------- LANDING PAGE ----------

# ---------- DASHBOARD ----------
def render_dashboard():
    # Top nav
    st.markdown(f"""
    <div class="top-nav">
        <div class="logo">⚡ Synapse AI</div>
        <div class="nav-right">
            <span style="color:rgba(255,255,255,0.4); font-size:0.85rem;">{st.session_state.username}</span>
            <div class="avatar">{st.session_state.username[0].upper()}<span class="status-dot"></span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar with only: Username, Logout, New Chat, Chat History
    with st.sidebar:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; padding:12px 14px; border-bottom:1px solid rgba(255,255,255,0.05); margin-bottom:16px;">
            <div style="width:40px; height:40px; border-radius:50%; background:linear-gradient(135deg, #a78bfa, #7c3aed); display:flex; align-items:center; justify-content:center; font-weight:700; color:white; font-size:1rem;">{st.session_state.username[0].upper()}</div>
            <div>
                <div style="color:white; font-weight:600; font-size:0.95rem;">{st.session_state.username}</div>
                <div style="color:rgba(255,255,255,0.3); font-size:0.7rem;">Online</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            logout_user()

        st.divider()

        if st.button("➕ New Chat", use_container_width=True):
            conv_id = str(int(time.time()))
            new_conv = {"id": conv_id, "name": "New Chat", "messages": []}
            st.session_state.conversations.append(new_conv)
            st.session_state.current_conv_id = conv_id
            save_user_conversations(st.session_state.username, st.session_state.conversations)
            st.rerun()

        st.divider()
        st.markdown("### 📂 Your Chats")

        for conv in st.session_state.conversations:
            is_active = conv["id"] == st.session_state.current_conv_id
            icon = "📌" if is_active else "💬"
            label = f"{icon} {conv['name']}"
            if st.button(label, key=f"conv_{conv['id']}", use_container_width=True):
                st.session_state.current_conv_id = conv["id"]
                st.rerun()

    # Main content


    # Stats cards
    st.markdown("""
    <div style="
        color:#ffffff;
        font-size:14px;
        font-weight:600;
        margin-top:-15px;
        margin-bottom:3px;
    ">
    Dashboard
    </div>
    """, unsafe_allow_html=True)

    # Get current conversation
    current_conv = None
    for conv in st.session_state.conversations:
        if conv["id"] == st.session_state.current_conv_id:
            current_conv = conv
            break
    if current_conv is None and st.session_state.conversations:
        current_conv = st.session_state.conversations[0]
        st.session_state.current_conv_id = current_conv["id"]
    elif current_conv is None:
        conv_id = str(int(time.time()))
        current_conv = {"id": conv_id, "name": "New Chat", "messages": []}
        st.session_state.conversations.append(current_conv)
        st.session_state.current_conv_id = conv_id
        save_user_conversations(st.session_state.username, st.session_state.conversations)

    st.markdown(f"""
    <div style="
        color:#ffffff;
        font-size:16px;
        font-weight:600;
        margin-top:-6px;
        margin-bottom:2px;
    ">
    💬 {current_conv["name"]}
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container()

    # Chat panel


    with chat_container:
        for msg in current_conv["messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
                if "sentiment" in msg:
                    sent = msg["sentiment"]
                    emoji = "😊" if sent == "Positive" else "😢" if sent == "Negative" else "😐"
                    badge_class = "positive" if sent == "Positive" else "negative" if sent == "Negative" else "neutral"
                    st.markdown(f'<div class="sentiment-badge {badge_class}">{emoji} {sent}</div>', unsafe_allow_html=True)



        # Input
    user_input = st.chat_input("✍️ Type your message...")
    if user_input:

        if not any(msg["role"] == "user" for msg in current_conv["messages"]):
            auto_name_conversation(current_conv, user_input)

        # Show user message immediately
        current_conv["messages"].append({
            "role": "user",
            "content": user_input
        })

        save_user_conversations(
            st.session_state.username,
            st.session_state.conversations
        )

        # Refresh so the user message appears instantly
        st.rerun()


    # Generate response only once
    if (
        current_conv["messages"]
        and current_conv["messages"][-1]["role"] == "user"
        and (
            len(current_conv["messages"]) == 1
            or current_conv["messages"][-2]["role"] == "assistant"
        )
    ):

        last_message = current_conv["messages"][-1]["content"]
        
        st.markdown("<div style='margin-top:-8px;'></div>", unsafe_allow_html=True)
        with st.spinner("🤔 Thinking..."):
            sentiment = get_sentiment(last_message)
            bot_response = get_response(last_message, sentiment)

        current_conv["messages"].append({
            "role": "assistant",
            "content": bot_response,
            "sentiment": sentiment
        })

        save_user_conversations(
            st.session_state.username,
            st.session_state.conversations
        )

        st.rerun()



# ---------- ROUTING ----------
if st.session_state.logged_in:
    render_dashboard()
else:
    render_auth_page()
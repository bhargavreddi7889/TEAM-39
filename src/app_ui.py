"""
CampusOps AI - Streamlit User Interface
========================================

A beautiful web interface for Admin and Student users.

Usage:
    cd src
    streamlit run app_ui.py
"""

import streamlit as st
import requests
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

API_BASE_URL = "http://brahamand.ai:9000"

# Demo credentials
USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "Administrator"},
    "student": {"password": "student123", "role": "student", "name": "Student User"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# Page Configuration
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="CampusOps AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Professional CSS with Google Fonts
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    h1, h2, h3, .main-header {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 2rem 0 0.5rem 0;
        letter-spacing: -0.02em;
        animation: fadeInDown 0.6s ease-out;
    }
    
    .sub-header {
        font-size: 1.25rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Dashboard Cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 1.5rem;
        color: white !important;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        color: white !important;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 0.5rem;
        animation: countUp 0.6s ease-out;
    }
    
    .stat-label {
        font-size: 1rem;
        color: white !important;
        opacity: 0.95;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Info Card Variations */
    .stat-card-primary {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    .stat-card-success {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    }
    
    .stat-card-warning {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
    }
    
    /* Chat Messages */
    .chat-user {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 1.5rem;
        border-radius: 1.25rem;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
        color: #1E293B !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
        animation: slideInRight 0.4s ease-out;
    }
    
    .chat-user:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.15);
    }
    
    .chat-user strong {
        color: #1E40AF !important;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    .chat-bot {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        padding: 1.5rem;
        border-radius: 1.25rem;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
        color: #1E293B !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
        transition: all 0.3s ease;
        animation: slideInLeft 0.4s ease-out;
    }
    
    .chat-bot:hover {
        transform: translateX(-5px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.15);
    }
    
    .chat-bot strong {
        color: #166534 !important;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    /* File Items */
    .file-item {
        background: white;
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #E2E8F0;
        margin: 0.75rem 0;
        color: #1E293B !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .file-item:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
    }
    
    .file-item strong {
        color: #0F172A !important;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 0.75rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 0.75rem;
        border: 2px solid #E2E8F0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.1);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        font-size: 0.9rem !important;
        padding: 0.6rem 1rem !important;
        height: auto !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateX(2px);
    }
    
    [data-testid="stSidebar"] .stRadio {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 0.75rem;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    [data-testid="stSidebar"] hr {
        background: rgba(255, 255, 255, 0.15) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Profile Card in Sidebar */
    .sidebar-profile-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar-profile-card h2 {
        margin: 0;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: white !important;
    }
    
    .sidebar-profile-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem !important;
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar Sections */
    .sidebar-section-title {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: rgba(255, 255, 255, 0.9) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 1.5rem 0 0.75rem 0 !important;
    }
    
    /* Sidebar Metrics */
    [data-testid="stSidebar"] .stMetric {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.75rem !important;
        border-radius: 0.75rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    [data-testid="stSidebar"] .stMetric label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.5);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #CBD5E1, transparent);
    }
    
    /* Metric Styling */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Session State
# ═══════════════════════════════════════════════════════════════════════════════

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ═══════════════════════════════════════════════════════════════════════════════
# API Functions
# ═══════════════════════════════════════════════════════════════════════════════

def api_health():
    try:
        r = requests.get(f"{API_BASE_URL}/", timeout=5)
        return r.status_code == 200, r.json()
    except:
        return False, None

def api_query(question):
    try:
        r = requests.post(f"{API_BASE_URL}/query/", json={"query": question}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_stats():
    try:
        r = requests.get(f"{API_BASE_URL}/admin/stats", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_list_files():
    try:
        r = requests.get(f"{API_BASE_URL}/admin/files", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_upload_file(file):
    try:
        files = {"file": (file.name, file.getvalue(), "text/plain")}
        r = requests.post(f"{API_BASE_URL}/admin/files", files=files, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_delete_file(filename):
    try:
        r = requests.delete(f"{API_BASE_URL}/admin/files/{filename}", timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def api_reindex(clear=True):
    try:
        r = requests.post(f"{API_BASE_URL}/admin/reindex", params={"clear_existing": clear}, timeout=120)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# Login Page
# ═══════════════════════════════════════════════════════════════════════════════

def show_login():
    # Hero Section
    st.markdown('''
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div style="font-size: 4rem; margin-bottom: 0.5rem;">🎓</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<p class="main-header">CampusOps AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Intelligent Campus Policy Assistant powered by AI</p>', unsafe_allow_html=True)
    
    # Check API
    api_ok, api_data = api_health()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if api_ok:
            st.success("✅ System Online & Ready", icon="✅")
        else:
            st.error("❌ API Server Not Running", icon="🚨")
            st.code("python run.py", language="bash")
            st.info("💡 **Tip:** Make sure the API server is running before logging in.")
            return
    
    # Login Form (removed extra whitespace)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["👨‍🎓 Student Login", "👨‍💼 Admin Login"])
        
        with tab1:
            st.markdown("### Welcome, Student!")
            
            with st.form("student_form"):
                user = st.text_input("👤 Username", key="s_user", placeholder="Enter your username")
                pwd = st.text_input("🔒 Password", type="password", key="s_pwd", placeholder="Enter your password")
                if st.form_submit_button("🚀 Sign In as Student", use_container_width=True, type="primary"):
                    if user in USERS and USERS[user]["password"] == pwd and USERS[user]["role"] == "student":
                        st.session_state.logged_in = True
                        st.session_state.user = USERS[user]["name"]
                        st.session_state.role = "student"
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
        
        with tab2:
            st.markdown("### Admin Portal")
            
            with st.form("admin_form"):
                user = st.text_input("👤 Username", key="a_user", placeholder="Enter admin username")
                pwd = st.text_input("🔒 Password", type="password", key="a_pwd", placeholder="Enter admin password")
                if st.form_submit_button("🚀 Sign In as Admin", use_container_width=True, type="primary"):
                    if user in USERS and USERS[user]["password"] == pwd and USERS[user]["role"] == "admin":
                        st.session_state.logged_in = True
                        st.session_state.user = USERS[user]["name"]
                        st.session_state.role = "admin"
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
    
    # Footer (reduced padding)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''
    <div style="text-align: center; color: #94A3B8; font-size: 0.9rem; padding: 1rem 0;">
        <p>🔒 Secure • 🚀 Fast • 🎯 Accurate</p>
        <p style="margin-top: 0.5rem;">Powered by AI & RAG Technology</p>
    </div>
    ''', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Student Interface
# ═══════════════════════════════════════════════════════════════════════════════

def show_student():
    # Sidebar
    with st.sidebar:
        # Profile Card
        st.markdown(f'''
        <div class="sidebar-profile-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👨‍🎓</div>
            <h2>Student Portal</h2>
            <p>{st.session_state.user}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Knowledge Base Stats
        st.markdown('<h3 class="sidebar-section-title">📊 Knowledge Base</h3>', unsafe_allow_html=True)
        stats = api_stats()
        if "error" not in stats:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Chunks", stats.get("total_chunks", 0))
            with col2:
                st.metric("Docs", stats.get("total_files", 0))
        
        st.divider()
        
        # Actions
        st.markdown('<h3 class="sidebar-section-title">⚙️ Actions</h3>', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.session_state.clear()
            st.rerun()
    
    # Main Content
    st.markdown('<p class="main-header">💬 Chat with CampusOps AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask me anything about campus policies, rules, and procedures</p>', unsafe_allow_html=True)
    
    # Input Section
    col1, col2 = st.columns([6, 1])
    default_q = st.session_state.pop("pending_question", "")
    
    with col1:
        question = st.text_input("Type your question here...", 
                                value=default_q, 
                                placeholder="e.g., What is the attendance policy for B.Tech students?", 
                                label_visibility="collapsed",
                                key="student_question_input")
    with col2:
        ask = st.button("🔍 Ask", use_container_width=True, type="primary")
    
    # Process Question
    if ask and question.strip():
        with st.spinner("🤔 Analyzing policy documents..."):
            result = api_query(question)
        
        if "error" not in result:
            st.session_state.chat_history.insert(0, {
                "q": question,
                "a": result.get("answer", "No answer available"),
                "sources": result.get("sources", []),
                "time": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
        else:
            st.error(f"❌ Error: {result['error']}")
    
    # Chat History
    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💬 Conversation History")
        
        for i, chat in enumerate(st.session_state.chat_history):
            # User Question
            st.markdown(f'''
            <div class="chat-user">
                <strong>🧑‍🎓 You</strong> 
                <span style="float: right; font-size: 0.85rem; opacity: 0.7;">{chat["time"]}</span>
                <br><br>
                {chat["q"]}
            </div>
            ''', unsafe_allow_html=True)
            
            # AI Response
            st.markdown('''
            <div class="chat-bot">
                <strong>🤖 CampusOps AI</strong>
                <br><br>
            ''', unsafe_allow_html=True)
            st.markdown(chat["a"])  # Render markdown properly
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sources
            if chat["sources"]:
                with st.expander(f"📚 View Sources ({len(chat['sources'])} documents)", expanded=False):
                    for j, src in enumerate(chat["sources"], 1):
                        st.markdown(f"**Source {j}:**")
                        st.text_area(f"source_{i}_{j}", src[:600] + "..." if len(src) > 600 else src, 
                                   height=100, key=f"src_{i}_{j}", disabled=True, label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        # Empty State
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("""
        👋 **Welcome to CampusOps AI!**
        
        Ask me anything about campus policies, rules, and procedures.
        
        💡 **Tip:** Type your question above to get started!
        """, icon="🎓")

# ═══════════════════════════════════════════════════════════════════════════════
# Admin Interface
# ═══════════════════════════════════════════════════════════════════════════════

def show_admin():
    with st.sidebar:
        # Profile Card
        st.markdown(f'''
        <div class="sidebar-profile-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👨‍💼</div>
            <h2>Admin Panel</h2>
            <p>{st.session_state.user}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Navigation
        st.markdown('<h3 class="sidebar-section-title">📍 Navigation</h3>', unsafe_allow_html=True)
        
        # Handle quick navigation from dashboard
        default_page = st.session_state.pop("quick_nav", "📊 Dashboard")
        page = st.radio("Select Page", ["📊 Dashboard", "📁 Files", "🔄 Re-index", "🔍 Test Query"], 
                       index=["📊 Dashboard", "📁 Files", "🔄 Re-index", "🔍 Test Query"].index(default_page) if default_page in ["📊 Dashboard", "📁 Files", "🔄 Re-index", "🔍 Test Query"] else 0,
                       label_visibility="collapsed")
        
        st.divider()
        
        # System Actions
        st.markdown('<h3 class="sidebar-section-title">⚙️ System</h3>', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.clear()
            st.rerun()
    
    if page == "📊 Dashboard":
        admin_dashboard()
    elif page == "📁 Files":
        admin_files()
    elif page == "🔄 Re-index":
        admin_reindex()
    elif page == "🔍 Test Query":
        admin_test()


def admin_dashboard():
    st.markdown('<p class="main-header">📊 Admin Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time insights into your campus knowledge base</p>', unsafe_allow_html=True)
    
    stats = api_stats()
    files = api_list_files()
    api_ok, _ = api_health()
    
    # Stats Cards with different colors
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown(f'''<div class="stat-card stat-card-primary">
            <div class="stat-number">📚 {stats.get("total_chunks", 0)}</div>
            <div class="stat-label">Knowledge Chunks</div>
        </div>''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''<div class="stat-card stat-card-success">
            <div class="stat-number">📄 {stats.get("total_files", 0)}</div>
            <div class="stat-label">Policy Documents</div>
        </div>''', unsafe_allow_html=True)
    
    with col3:
        status = "🟢" if api_ok else "🔴"
        status_text = "Online" if api_ok else "Offline"
        card_class = "stat-card stat-card-success" if api_ok else "stat-card stat-card-warning"
        st.markdown(f'''<div class="{card_class}">
            <div class="stat-number">{status}</div>
            <div class="stat-label">System {status_text}</div>
        </div>''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        if st.button("📤 Upload File", use_container_width=True, type="primary"):
            st.session_state.quick_nav = "📁 Files"
            st.rerun()
    
    with col2:
        if st.button("🔄 Re-index", use_container_width=True):
            st.session_state.quick_nav = "🔄 Re-index"
            st.rerun()
    
    with col3:
        if st.button("🔍 Test Query", use_container_width=True):
            st.session_state.quick_nav = "🔍 Test Query"
            st.rerun()
    
    with col4:
        if st.button("📊 Refresh Stats", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Files Overview with enhanced styling
    st.markdown("### 📁 Documents Library")
    
    if "error" not in files and files.get("files"):
        file_list = files.get("files", [])
        
        # Display as cards
        for idx, f in enumerate(file_list):
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.markdown(f'''
                <div class="file-item">
                    📄 <strong>{f["filename"]}</strong>
                    <br><small style="color: #64748B; font-size: 0.85rem;">
                        Size: {f["size_bytes"]:,} bytes
                    </small>
                </div>
                ''', unsafe_allow_html=True)
            with col2:
                if st.button("👁️ View", key=f"view_dash_{idx}", use_container_width=True):
                    st.session_state.view_file_dash = f['filename']
            with col3:
                if st.button("🗑️ Delete", key=f"del_dash_{idx}", use_container_width=True):
                    st.session_state.delete_file_dash = f['filename']
        
        # Handle view
        if "view_file_dash" in st.session_state:
            fn = st.session_state.view_file_dash
            st.markdown(f"### 📖 Viewing: {fn}")
            try:
                r = requests.get(f"{API_BASE_URL}/admin/files/{fn}")
                st.text_area("Content", r.text, height=300, disabled=True)
            except Exception as e:
                st.error(str(e))
            if st.button("✖️ Close"):
                del st.session_state.view_file_dash
                st.rerun()
        
        # Handle delete
        if "delete_file_dash" in st.session_state:
            fn = st.session_state.delete_file_dash
            st.warning(f"⚠️ Are you sure you want to delete **{fn}**?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Confirm Delete", type="primary", use_container_width=True):
                    result = api_delete_file(fn)
                    if "error" not in result:
                        st.success("✅ File deleted successfully!")
                    del st.session_state.delete_file_dash
                    st.rerun()
            with c2:
                if st.button("❌ Cancel", use_container_width=True):
                    del st.session_state.delete_file_dash
                    st.rerun()
    elif "error" in files:
        st.error("❌ Failed to load files")
    else:
        st.info("📂 No documents yet. Upload your first policy document to get started!")
        if st.button("➕ Upload First Document", type="primary"):
            st.session_state.quick_nav = "📁 Files"
            st.rerun()


def admin_files():
    st.markdown('<p class="main-header">📁 File Management</p>', unsafe_allow_html=True)
    
    # Upload
    st.markdown("### ⬆️ Upload New File")
    st.caption("Supported formats: .txt, .docx, .pdf")
    uploaded = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])
    
    if uploaded:
        file_ext = uploaded.name.split('.')[-1].lower()
        st.info(f"Selected: {uploaded.name} ({uploaded.size} bytes) - Type: .{file_ext}")
        
        # Preview (only for text files)
        if file_ext == "txt":
            with st.expander("📖 Preview"):
                try:
                    st.text(uploaded.getvalue().decode("utf-8")[:1000])
                except:
                    st.warning("Could not preview file")
        elif file_ext == "docx":
            st.caption("📄 Word document - preview not available")
        elif file_ext == "pdf":
            st.caption("📑 PDF document - preview not available")
        
        if st.button("📤 Upload & Index", type="primary"):
            with st.spinner("Uploading and extracting text..."):
                result = api_upload_file(uploaded)
            
            if "error" not in result:
                st.success(f"✅ {result.get('message', 'Uploaded!')}")
                st.info(f"Chunks added: {result.get('chunks_added', 0)}")
                st.rerun()
            else:
                st.error(f"Error: {result['error']}")
    
    st.divider()
    
    # File list
    st.markdown("### 📋 Existing Files")
    files = api_list_files()
    
    if "error" not in files:
        file_list = files.get("files", [])
        if file_list:
            for f in file_list:
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.markdown(f'<div class="file-item">📄 <strong>{f["filename"]}</strong> ({f["size_bytes"]} bytes)</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("👁️", key=f"view_{f['filename']}", help="View"):
                        st.session_state.view_file = f['filename']
                with col3:
                    if st.button("🗑️", key=f"del_{f['filename']}", help="Delete"):
                        st.session_state.delete_file = f['filename']
            
            # View file
            if "view_file" in st.session_state:
                fn = st.session_state.view_file
                st.markdown(f"### 📖 {fn}")
                try:
                    r = requests.get(f"{API_BASE_URL}/admin/files/{fn}")
                    st.text_area("Content", r.text, height=300, disabled=True)
                except Exception as e:
                    st.error(str(e))
                if st.button("Close"):
                    del st.session_state.view_file
                    st.rerun()
            
            # Delete confirm
            if "delete_file" in st.session_state:
                fn = st.session_state.delete_file
                st.warning(f"Delete **{fn}**?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Yes", type="primary"):
                        result = api_delete_file(fn)
                        if "error" not in result:
                            st.success("Deleted!")
                        del st.session_state.delete_file
                        st.rerun()
                with c2:
                    if st.button("❌ No"):
                        del st.session_state.delete_file
                        st.rerun()
        else:
            st.info("No files yet. Upload one above!")
    else:
        st.error("Failed to load files")


def admin_reindex():
    st.markdown('<p class="main-header">🔄 Re-index Knowledge Base</p>', unsafe_allow_html=True)
    
    st.markdown("""
    Use this when:
    - Files were manually added to `data/`
    - Database seems out of sync
    - You want to rebuild the index
    """)
    
    stats = api_stats()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Chunks", stats.get("total_chunks", 0))
    with col2:
        st.metric("Total Files", stats.get("total_files", 0))
    
    st.divider()
    
    clear = st.checkbox("Clear existing database first", value=True)
    st.warning("⚠️ This may take a few minutes.")
    
    if st.button("🔄 Start Re-indexing", type="primary", use_container_width=True):
        with st.spinner("Re-indexing all files..."):
            result = api_reindex(clear)
        
        if "error" not in result:
            st.success(f"✅ {result.get('message', 'Done!')}")
            
            for f in result.get("files_processed", []):
                if "error" in f:
                    st.error(f"❌ {f['filename']}: {f['error']}")
                else:
                    st.success(f"✅ {f['filename']}: {f['chunks']} chunks")
            
            st.metric("Total Chunks", result.get("total_chunks", 0))
        else:
            st.error(f"Error: {result['error']}")


def admin_test():
    st.markdown('<p class="main-header">🔍 Test Query</p>', unsafe_allow_html=True)
    
    question = st.text_input("Enter a test question", placeholder="e.g., What is the attendance policy?")
    
    if st.button("🔍 Test", type="primary"):
        if question:
            with st.spinner("Processing..."):
                result = api_query(question)
            
            if "error" not in result:
                st.markdown("### 📝 Answer")
                # Use markdown to render bullet points properly
                st.markdown(result.get("answer", "No answer"))
                
                st.markdown("### 📚 Sources")
                for i, src in enumerate(result.get("sources", [])):
                    with st.expander(f"Source {i+1}"):
                        st.text(src)
            else:
                st.error(result["error"])

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if not st.session_state.logged_in:
        show_login()
    elif st.session_state.role == "student":
        show_student()
    elif st.session_state.role == "admin":
        show_admin()
    else:
        st.session_state.logged_in = False
        st.rerun()

if __name__ == "__main__":
    main()

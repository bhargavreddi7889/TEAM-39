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

API_BASE_URL = "http://localhost:8000"

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

# Custom CSS with high contrast colors
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white !important;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: white !important;
    }
    .stat-label {
        font-size: 0.9rem;
        color: white !important;
        opacity: 0.9;
    }
    .chat-user {
        background-color: #DBEAFE !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2563EB;
        margin: 0.5rem 0;
        color: #000000 !important;
    }
    .chat-user strong {
        color: #1E40AF !important;
    }
    .chat-bot {
        background-color: #DCFCE7 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #16A34A;
        margin: 0.5rem 0;
        color: #000000 !important;
    }
    .chat-bot strong {
        color: #166534 !important;
    }
    .file-item {
        background-color: #F1F5F9 !important;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #CBD5E1;
        margin: 0.25rem 0;
        color: #000000 !important;
    }
    .file-item strong {
        color: #1E293B !important;
    }
    /* Force black text in chat messages */
    .chat-user, .chat-user * {
        color: #000000 !important;
    }
    .chat-user strong {
        color: #1E40AF !important;
    }
    .chat-bot, .chat-bot * {
        color: #000000 !important;
    }
    .chat-bot strong {
        color: #166534 !important;
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
    st.markdown('<p class="main-header">🎓 CampusOps AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent Campus Policy Assistant</p>', unsafe_allow_html=True)
    
    # Check API
    api_ok, _ = api_health()
    if api_ok:
        st.success("✅ API Server is running")
    else:
        st.error("❌ API Server is not running")
        st.code("cd src && uvicorn main:app --reload --port 8000", language="bash")
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        tab1, tab2 = st.tabs(["👨‍🎓 Student", "👨‍💼 Admin"])
        
        with tab1:
            st.info("Demo: `student` / `student123`")
            with st.form("student_form"):
                user = st.text_input("Username", key="s_user")
                pwd = st.text_input("Password", type="password", key="s_pwd")
                if st.form_submit_button("Login as Student", use_container_width=True):
                    if user in USERS and USERS[user]["password"] == pwd and USERS[user]["role"] == "student":
                        st.session_state.logged_in = True
                        st.session_state.user = USERS[user]["name"]
                        st.session_state.role = "student"
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            st.info("Demo: `admin` / `admin123`")
            with st.form("admin_form"):
                user = st.text_input("Username", key="a_user")
                pwd = st.text_input("Password", type="password", key="a_pwd")
                if st.form_submit_button("Login as Admin", use_container_width=True):
                    if user in USERS and USERS[user]["password"] == pwd and USERS[user]["role"] == "admin":
                        st.session_state.logged_in = True
                        st.session_state.user = USERS[user]["name"]
                        st.session_state.role = "admin"
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

# ═══════════════════════════════════════════════════════════════════════════════
# Student Interface
# ═══════════════════════════════════════════════════════════════════════════════

def show_student():
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👨‍🎓 {st.session_state.user}")
        st.divider()
        
        stats = api_stats()
        if "error" not in stats:
            st.metric("📚 Chunks", stats.get("total_chunks", 0))
            st.metric("📄 Files", stats.get("total_files", 0))
        
        st.divider()
        st.markdown("### 💡 Try asking:")
        questions = [
            "What is the minimum attendance?",
            "What are the exam rules?",
            "Tell me about placement policy",
            "When does semester start?",
        ]
        for q in questions:
            if st.button(q, key=f"q_{q[:15]}", use_container_width=True):
                st.session_state.pending_question = q
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.rerun()
    
    # Main
    st.markdown('<p class="main-header">🎓 Ask About Campus Policies</p>', unsafe_allow_html=True)
    
    # Input
    col1, col2 = st.columns([5, 1])
    default_q = st.session_state.pop("pending_question", "")
    
    with col1:
        question = st.text_input("Your question", value=default_q, placeholder="e.g., What is the attendance policy?", label_visibility="collapsed")
    with col2:
        ask = st.button("🔍 Ask", use_container_width=True, type="primary")
    
    if ask and question:
        with st.spinner("🤔 Thinking..."):
            result = api_query(question)
        
        if "error" not in result:
            st.session_state.chat_history.insert(0, {
                "q": question,
                "a": result.get("answer", "No answer"),
                "sources": result.get("sources", []),
                "time": datetime.now().strftime("%H:%M")
            })
    
    # Chat history
    if st.session_state.chat_history:
        st.divider()
        for i, chat in enumerate(st.session_state.chat_history):
            st.markdown(f'<div class="chat-user"><strong>🧑‍🎓 You</strong> ({chat["time"]})<br>{chat["q"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bot"><strong>🤖 CampusOps AI</strong><br>{chat["a"]}</div>', unsafe_allow_html=True)
            
            if chat["sources"]:
                with st.expander(f"📚 Sources ({len(chat['sources'])})"):
                    for j, src in enumerate(chat["sources"]):
                        st.text_area(f"Source {j+1}", src[:500], height=80, key=f"src_{i}_{j}", disabled=True)
            st.divider()
        
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# Admin Interface
# ═══════════════════════════════════════════════════════════════════════════════

def show_admin():
    with st.sidebar:
        st.markdown(f"### 👨‍💼 {st.session_state.user}")
        st.divider()
        
        page = st.radio("Navigation", ["📊 Dashboard", "📁 Files", "🔄 Re-index", "🔍 Test Query"], label_visibility="collapsed")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
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
    
    stats = api_stats()
    files = api_list_files()
    api_ok, _ = api_health()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''<div class="stat-card">
            <div class="stat-number">{stats.get("total_chunks", 0)}</div>
            <div class="stat-label">Total Chunks</div>
        </div>''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''<div class="stat-card">
            <div class="stat-number">{stats.get("total_files", 0)}</div>
            <div class="stat-label">Policy Files</div>
        </div>''', unsafe_allow_html=True)
    
    with col3:
        status = "🟢 Online" if api_ok else "🔴 Offline"
        st.markdown(f'''<div class="stat-card">
            <div class="stat-number">{status}</div>
            <div class="stat-label">API Status</div>
        </div>''', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 📁 Files Overview")
    
    if "error" not in files:
        for f in files.get("files", []):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"📄 **{f['filename']}**")
            with col2:
                st.caption(f"{f['size_bytes']} bytes")
    else:
        st.error("Failed to load files")


def admin_files():
    st.markdown('<p class="main-header">📁 File Management</p>', unsafe_allow_html=True)
    
    # Upload
    st.markdown("### ⬆️ Upload New File")
    uploaded = st.file_uploader("Choose a .txt file", type=["txt"])
    
    if uploaded:
        st.info(f"Selected: {uploaded.name} ({uploaded.size} bytes)")
        
        with st.expander("📖 Preview"):
            st.text(uploaded.getvalue().decode("utf-8")[:1000])
        
        if st.button("📤 Upload & Index", type="primary"):
            with st.spinner("Uploading..."):
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
                st.info(result.get("answer", "No answer"))
                
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

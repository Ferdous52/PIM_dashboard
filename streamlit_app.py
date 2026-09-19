import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PIM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False



def login_page():

    st.markdown("""
    <style>
    .stApp {background:linear-gradient(135deg,#0F172A 0%,#172554 50%,#0F172A 100%) !important;}
    .main .block-container {min-height: 100vh;box-sizing: border-box;display: flex;flex-direction: column;justify-content: center;padding-top: 30px !important;padding-bottom: 30px !important;}
    .pim-title {text-align: center;color: white;font-size: 42px;font-weight: 700;margin-top: 0;margin-bottom: 5px;}
    .pim-subtitle {text-align: center;color: #CBD5E1;font-size: 17px;margin-bottom: 30px;}

    [data-testid="stForm"] {background: rgba(15, 23, 42, 0.95);padding: 30px !important;border-radius: 18px;border: 1px solid rgba(255,255,255,0.18);box-shadow: 0px 10px 40px rgba(0,0,0,0.45);}
    [data-testid="stForm"] label {color: #E5E7EB !important;font-weight: 500;}
    [data-testid="stForm"] input {background-color: rgba(255,255,255,0.08) !important;color: white !important;border: 1px solid rgba(255,255,255,0.20) !important;border-radius: 8px !important;}
    [data-testid="stForm"] input::placeholder {color: #94A3B8 !important;}
    [data-testid="stFormSubmitButton"] button {width: 100%;background-color: #2563EB;color: white;border: none;border-radius: 8px;padding: 10px;font-size: 16px;font-weight: 600;}
    [data-testid="stFormSubmitButton"] button:hover {background-color: #1D4ED8;color: white;}

    </style>
    """, unsafe_allow_html=True)



    st.markdown('<div class="pim-title">📊 PIM Dashboard</div>',unsafe_allow_html=True)

    st.markdown("""<div class="pim-subtitle">Monitor &nbsp;•&nbsp; Analyze &nbsp;•&nbsp; Improve</div>""",unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.1, 1])
    with center:
        st.markdown("""<div style="text-align:center;color:#FFFFFF;font-size:24px;font-weight:600;margin-bottom:8px;">Welcome Back!</div>""",unsafe_allow_html=True)
        st.markdown("""<div style="text-align:center;color:#CBD5E1;font-size:14px;margin-bottom:15px;">Sign in to access the PIM Dashboard</div>""",unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username",placeholder="Enter your username")
            password = st.text_input("Password",type="password",placeholder="Enter your password")
            login_button = st.form_submit_button("🔐 Login")
        if login_button:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.page = "upload"
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    return login_page()

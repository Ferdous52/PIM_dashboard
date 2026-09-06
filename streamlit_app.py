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

st.markdown("""
    <style>

    .stApp {background:linear-gradient(135deg,
                                       #0F172A 0%,
                                       #172554 50%,
                                       #0F172A 100%)!important;
        }
        
    .main .block-container {min-height: 100vh;
                            box-sizing: border-box;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            padding-top: 30px !important;
                            padding-bottom: 30px !important;}
    </style>""", unsafe_allow_html=True)

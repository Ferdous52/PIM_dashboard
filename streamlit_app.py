import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PIM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def page_style():
    return  ("""<style>.stApp{background: #F8FAFC;}.stSelectbox{background: #8F172A;}</style>""")



st.markdown(page_style(),unsafe_allow_html=True)

st.selectbox("Label",options=("Option 1", "Option 2", "Option 3"))

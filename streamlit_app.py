import streamlit as st


def page_setup():
    page_setup = (page_title="PIM Dashboard",page_icon="📊",layout="wide",initial_sidebar_state="collapsed")
    return page_setup
    
def page_style():
    page = ("""<style>.stApp{background: #2F172F;}</style>""")
    return  page


st.set_page_config(page_setup)
st.markdown(page_style(),unsafe_allow_html=True)
st.balloons()
on = st.toggle("Activate feature")




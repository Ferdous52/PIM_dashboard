import streamlit as st



def page_style():
   page_style = ("""\<style>.stApp{background: #2F172F;}\</style>""")
   return page_style

st.set_page_config(page_title="PIM Dashboard",page_icon="📊",layout="wide",initial_sidebar_state="collapsed")
st.markdown(page_style(), unsafe_allow_html=True)

st.balloons()

on = st.toggle("Activate feature")

if on:
    st.write("Feature activated!")

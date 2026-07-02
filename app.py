import streamlit as st

from state import init_session_state
from styles import apply_global_styles

st.set_page_config(page_title="Handball Team Hub", layout="centered")
apply_global_styles()
init_session_state()

st.markdown('<div class="main-title">HANDBALL TEAM HUB</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
st.write("Open each page directly:")
st.code("streamlit run training.py")
st.code("streamlit run today.py")
st.code("streamlit run admin.py")

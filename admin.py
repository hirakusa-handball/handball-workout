import streamlit as st

from pages.admin import render_admin_page
from state import init_session_state
from styles import apply_global_styles

st.set_page_config(page_title="Administration", layout="centered")
apply_global_styles()
init_session_state()
render_admin_page()

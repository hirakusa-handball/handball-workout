import streamlit as st

from pages.admin import render_admin_page
from pages.today import render_todays_training_page
from pages.training import render_training_page
from state import init_session_state
from styles import apply_global_styles

st.set_page_config(page_title="Handball Team Hub", layout="centered")
apply_global_styles()
init_session_state()

st.sidebar.title("Menu")
page = st.sidebar.radio("Select page", ["Training", "Today's Workout", "Admin"])

if page == "Training":
    render_training_page()
elif page == "Today's Workout":
    render_todays_training_page()
elif page == "Admin":
    render_admin_page()

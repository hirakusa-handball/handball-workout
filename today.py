import streamlit as st

from pages.today import render_todays_training_page
from state import init_session_state
from styles import apply_global_styles

st.set_page_config(page_title="Today's Workout", layout="centered")
apply_global_styles()
init_session_state()
render_todays_training_page()

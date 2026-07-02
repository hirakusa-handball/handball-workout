import streamlit as st

from pages.admin import render_admin_page
from pages.today import render_todays_training_page
from pages.training import render_training_page
from state import init_session_state
from styles import apply_global_styles

st.set_page_config(page_title="Handball Team Hub", layout="centered")
apply_global_styles()
init_session_state()

st.sidebar.title("メニュー")
page = st.sidebar.radio("ページを選択", ["トレーニング", "本日のトレーニング", "管理者"])

if page == "トレーニング":
    render_training_page()
elif page == "本日のトレーニング":
    render_todays_training_page()
elif page == "管理者":
    render_admin_page()

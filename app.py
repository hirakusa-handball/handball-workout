import streamlit as st

from pages.admin import render_admin_page
from pages.today import render_todays_training_page
from pages.training import render_training_page
from state import init_session_state
from styles import apply_global_styles

ADMIN_PASSWORD = "8102"

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
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if not st.session_state["admin_authenticated"]:
        st.warning("Admin page is password protected.")
        password = st.text_input("Enter admin password", type="password")
        if st.button("Unlock Admin"):
            if password == ADMIN_PASSWORD:
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        st.stop()

    render_admin_page()

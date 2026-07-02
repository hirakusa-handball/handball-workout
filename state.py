import streamlit as st
from copy import deepcopy

from defaults import DEFAULT_LIBRARY, DEFAULT_TODAYS_MENU


def init_session_state() -> None:
    if "library" not in st.session_state:
        st.session_state["library"] = deepcopy(DEFAULT_LIBRARY)

    if "todays_menu" not in st.session_state:
        st.session_state["todays_menu"] = deepcopy(DEFAULT_TODAYS_MENU)

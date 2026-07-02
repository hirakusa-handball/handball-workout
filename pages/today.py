import streamlit as st


def render_todays_training_page() -> None:
    st.markdown('<div class="main-title">TODAY\'S WORKOUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Today\'s Menu</div>', unsafe_allow_html=True)

    if not st.session_state["todays_menu"]:
        st.write("No workout has been set for today yet.")
        return

    for index, today_item in enumerate(st.session_state["todays_menu"]):
        library_match = next(
            (
                lib
                for lib in st.session_state["library"]
                if lib["id"] == today_item.get("library_id")
            ),
            None,
        )
        display_name = today_item.get("name", "Unknown workout")
        display_title = f"{index + 1}. {display_name} | {today_item['reps']} reps x {today_item['sets']} sets"

        with st.expander(display_title):
            if library_match:
                st.video(library_match["url"])
                if library_match["point"]:
                    st.caption(f"Tip: {library_match['point']}")
            else:
                st.error("Original workout data no longer exists in the library.")

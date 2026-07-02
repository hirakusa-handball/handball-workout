import streamlit as st

from constants import CATEGORIES, CATEGORY_LABELS
from repository import sheets_repository
from state import refresh_session_state_from_storage


def render_admin_page() -> None:
    st.markdown('<div class="main-title">ADMINISTRATION</div>', unsafe_allow_html=True)
    render_todays_menu_admin()
    st.divider()
    render_library_create_admin()
    st.divider()
    render_library_edit_admin()


def render_todays_menu_admin() -> None:
    st.markdown('<div class="section-header">Build Today\'s Workout</div>', unsafe_allow_html=True)

    available_names = [item["name"] for item in st.session_state["library"]]
    library_by_name = {item["name"]: item for item in st.session_state["library"]}
    with st.form(key="add_today_form"):
        if available_names:
            selected_name = st.selectbox("Select a workout from the library", available_names)
            col1, col2 = st.columns(2)
            with col1:
                target_reps = st.text_input("Reps (e.g. 10 or 8-10)")
            with col2:
                target_sets = st.text_input("Sets (e.g. 3)")

            submit_today = st.form_submit_button(label="Add to today's menu")
            if submit_today:
                if target_reps and target_sets:
                    selected_item = library_by_name.get(selected_name)
                    if not selected_item:
                        st.error("Selected workout was not found.")
                    else:
                        try:
                            sheets_repository.add_todays_menu_item(
                                library_id=selected_item["id"],
                                reps=target_reps,
                                sets=target_sets,
                            )
                            refresh_session_state_from_storage()
                            st.success(f"Added '{selected_name}' to today's menu.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Failed to save: {exc}")
                else:
                    st.error("Please enter both reps and sets.")
        else:
            st.warning("Add workouts to the library first.")

    if st.button("Clear today's menu"):
        try:
            sheets_repository.clear_todays_menu()
            refresh_session_state_from_storage()
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to clear: {exc}")


def render_library_create_admin() -> None:
    st.markdown('<div class="section-header">Add Workout to Library</div>', unsafe_allow_html=True)
    with st.form(key="add_library_form"):
        new_cat = st.selectbox("Category", CATEGORIES, format_func=lambda c: CATEGORY_LABELS[c])
        new_name = st.text_input("Workout name (e.g. Pull-up)")
        new_url = st.text_input("Video URL (YouTube link, etc.)")
        new_point = st.text_area("Coaching tip (optional)")

        submit_lib = st.form_submit_button(label="Add to library")
        if submit_lib:
            if new_name and new_url:
                if any(item["name"] == new_name for item in st.session_state["library"]):
                    st.error("That workout name already exists. Please use a different name.")
                else:
                    try:
                        sheets_repository.add_library_item(
                            category=new_cat,
                            name=new_name,
                            url=new_url,
                            point=new_point,
                        )
                        refresh_session_state_from_storage()
                        st.success(f"Added '{new_name}' to the {CATEGORY_LABELS[new_cat]} category.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Failed to register: {exc}")
            else:
                st.error("Workout name and video URL are required.")


def render_library_edit_admin() -> None:
    st.markdown('<div class="section-header">Edit or Delete Library Workout</div>', unsafe_allow_html=True)
    available_names = [item["name"] for item in st.session_state["library"]]
    if not available_names:
        st.write("No workouts are currently registered in the library.")
        return

    edit_target_name = st.selectbox(
        "Select workout to edit or delete",
        available_names,
        key="edit_select",
    )

    if not edit_target_name:
        return

    target_index = next(
        (i for i, item in enumerate(st.session_state["library"]) if item["name"] == edit_target_name),
        -1,
    )
    if target_index < 0:
        st.error("Target workout was not found.")
        return
    target_item = st.session_state["library"][target_index]

    with st.form(key="edit_lib_form"):
        edit_cat = st.selectbox(
            "Category",
            CATEGORIES,
            index=CATEGORIES.index(target_item["category"]),
            format_func=lambda c: CATEGORY_LABELS[c],
        )
        edit_name = st.text_input("Workout name", value=target_item["name"])
        edit_url = st.text_input("Video URL", value=target_item["url"])
        edit_point = st.text_area("Coaching tip", value=target_item["point"])
        submit_update = st.form_submit_button("Update workout")

    delete_btn = st.button("Delete this workout from library")

    if submit_update:
        if edit_name and edit_url:
            conflict = any(
                item["name"] == edit_name and i != target_index
                for i, item in enumerate(st.session_state["library"])
            )
            if conflict:
                st.error("That workout name is already used by another item.")
            else:
                try:
                    sheets_repository.update_library_item(
                        item_id=target_item["id"],
                        category=edit_cat,
                        name=edit_name,
                        url=edit_url,
                        point=edit_point,
                    )
                    refresh_session_state_from_storage()
                    st.success("Library workout updated.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Failed to update: {exc}")
        else:
            st.error("Workout name and video URL are required.")

    if delete_btn:
        try:
            sheets_repository.delete_library_item(target_item["id"])
            refresh_session_state_from_storage()
            st.success(f"Deleted '{edit_target_name}'.")
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to delete: {exc}")

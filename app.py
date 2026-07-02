import streamlit as st

from constants import CATEGORIES, CATEGORY_LABELS
from repository import sheets_repository
from state import refresh_session_state_from_storage
from state import init_session_state
from styles import apply_global_styles

ADMIN_PASSWORD = "8102"

st.set_page_config(page_title="Handball Team Hub", layout="centered")
apply_global_styles()
init_session_state()

st.sidebar.title("Menu")
page = st.sidebar.radio("Select page", ["Training", "Today's Workout", "Admin"])


def render_training_page() -> None:
    st.markdown('<div class="main-title">TRAINING LIBRARY</div>', unsafe_allow_html=True)
    st.write("This is your team's training exercise library.")

    tabs = st.tabs([CATEGORY_LABELS[cat] for cat in CATEGORIES])
    for i, cat in enumerate(CATEGORIES):
        with tabs[i]:
            st.markdown(
                f'<div class="section-header">{CATEGORY_LABELS[cat]} Menu</div>',
                unsafe_allow_html=True,
            )
            # --- 変更箇所：筋力タブの場合のみサブメニューを表示 ---
            if cat == "筋力":  # ← 画面のラベルではなく、変数(cat)自体で判定します
                sub_cat = st.radio("部位を選択", ["Push", "Pull", "Leg"], horizontal=True, key=f"radio_{cat}")
                target_cat_string = f"{cat}_{sub_cat}"
                cat_items = [item for item in st.session_state["library"] if item["category"] == target_cat_string]
            else:
                cat_items = [item for item in st.session_state["library"] if item["category"] == cat]
            # --------------------------------------------------
            if not cat_items:
                st.caption("No exercises registered in this category yet.")
                continue

            for item in cat_items:
                with st.expander(item["name"]):
                    st.video(item["url"])
                    if item["point"]:
                        st.caption(f"Tip: {item['point']}")


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
    
    # フォームの外でカテゴリーを選択させる（切り替えると画面が反応するようにするため）
    new_cat = st.selectbox("Category", CATEGORIES, format_func=lambda c: CATEGORY_LABELS[c])
    new_sub_cat = ""
    # 変更前: if CATEGORY_LABELS[new_cat] == "筋力":
    if new_cat == "筋力":
        new_sub_cat = st.selectbox("部位", ["Push", "Pull", "Leg"], key="create_sub")

    with st.form(key="add_library_form"):
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
                        # 筋力の場合は「strength_Push」のように結合して保存
                        save_cat = f"{new_cat}_{new_sub_cat}" if new_sub_cat else new_cat
                        
                        sheets_repository.add_library_item(
                            category=save_cat,
                            name=new_name,
                            url=new_url,
                            point=new_point,
                        )
                        refresh_session_state_from_storage()
                        st.success(f"Added '{new_name}' to the library.")
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

    edit_target_name = st.selectbox("Select workout to edit or delete", available_names, key="edit_select")

    if not edit_target_name:
        return

    target_index = next((i for i, item in enumerate(st.session_state["library"]) if item["name"] == edit_target_name), -1)
    if target_index < 0:
        st.error("Target workout was not found.")
        return
    
    target_item = st.session_state["library"][target_index]

    # 保存されている文字列（例: strength_Push）を分解する
    raw_cat = target_item["category"]
    if "_" in raw_cat:
        base_cat, base_sub = raw_cat.split("_", 1)
    else:
        base_cat, base_sub = raw_cat, "Push" # 古いデータ用

    # フォームの外でカテゴリーを選択
    edit_cat = st.selectbox(
        "Category",
        CATEGORIES,
        index=CATEGORIES.index(base_cat) if base_cat in CATEGORIES else 0,
        format_func=lambda c: CATEGORY_LABELS[c],
        key="edit_cat_select"
    )
    
    edit_sub_cat = ""
    # 変更前: if CATEGORY_LABELS[edit_cat] == "筋力":
    if edit_cat == "筋力":
        sub_options = ["Push", "Pull", "Leg"]
        edit_sub_cat = st.selectbox("部位", sub_options, index=sub_options.index(base_sub) if base_sub in sub_options else 0, key="edit_sub")
    with st.form(key="edit_lib_form"):
        edit_name = st.text_input("Workout name", value=target_item["name"])
        edit_url = st.text_input("Video URL", value=target_item["url"])
        edit_point = st.text_area("Coaching tip", value=target_item["point"])
        submit_update = st.form_submit_button("Update workout")

    delete_btn = st.button("Delete this workout from library")

    if submit_update:
        if edit_name and edit_url:
            conflict = any(item["name"] == edit_name and i != target_index for i, item in enumerate(st.session_state["library"]))
            if conflict:
                st.error("That workout name is already used by another item.")
            else:
                try:
                    # 再び合体させて保存
                    save_cat = f"{edit_cat}_{edit_sub_cat}" if edit_sub_cat else edit_cat
                    
                    sheets_repository.update_library_item(
                        item_id=target_item["id"],
                        category=save_cat,
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

import streamlit as st
from datetime import date
import re  # ★追加：URLの中からIDを探し出すためのツール

from constants import CATEGORIES, CATEGORY_LABELS
from repository import sheets_repository
from state import refresh_session_state_from_storage
from state import init_session_state
from styles import apply_global_styles

ADMIN_PASSWORD = "8102"

st.set_page_config(page_title="Handball Team Hub", layout="centered")
st.markdown(
    """
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="theme-color" content="#000000">
    </head>
    """,
    unsafe_allow_html=True,
)
apply_global_styles()
init_session_state()

st.sidebar.title("Menu")
page = st.sidebar.radio("Select page", ["Training", "Daily Workout", "Admin"])

# ★追加：動画を正しく表示するための専用関数
# ★変更：動画を綺麗に表示するための専用関数（スマホ最適化版）
def display_media(url: str) -> None:
    if not url:
        return
    
    if "drive.google.com/file/d/" in url:
        match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
        if match:
            file_id = match.group(1)
            # スマホの縦長動画（9:16）がすっぽり収まるように枠を自動計算させる
            iframe_html = f'''
            <div style="width: 100%; aspect-ratio: 9/16; max-height: 80vh; overflow: hidden; border-radius: 8px;">
                <iframe src="https://drive.google.com/file/d/{file_id}/preview" width="100%" height="100%" style="border:none;"></iframe>
            </div>
            '''
            st.markdown(iframe_html, unsafe_allow_html=True)
        else:
            st.write(url)
    else:
        # YouTubeなどの場合は綺麗にネイティブ再生
        st.video(url)

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
            if cat == "筋力":
                sub_cat = st.radio("部位を選択", ["Push", "Pull", "Leg"], horizontal=True, key=f"radio_{cat}")
                target_cat_string = f"{cat}_{sub_cat}"
                cat_items = [item for item in st.session_state["library"] if item["category"] == target_cat_string]
            else:
                cat_items = [item for item in st.session_state["library"] if item["category"] == cat]
            
            if not cat_items:
                st.caption("No exercises registered in this category yet.")
                continue

            for item in cat_items:
                with st.expander(item["name"]):
                    # ★変更：先ほど作った専用関数を使って表示する
                    display_media(item["url"])
                    
                    if item["point"]:
                        st.caption(f"Tip: {item['point']}")


def render_todays_training_page() -> None:
    st.markdown('<div class="main-title">WORKOUT SCHEDULE</div>', unsafe_allow_html=True)
    
    selected_date = st.date_input("カレンダーから日付を選択", date.today(), key="view_date")
    date_str = selected_date.isoformat()
    
    st.markdown(f'<div class="section-header">{date_str} のメニュー</div>', unsafe_allow_html=True)

    current_menu = sheets_repository.get_todays_menu(date_str)

    if not current_menu:
        st.write("この日のトレーニングはまだ設定されていません。")
        return

    for index, today_item in enumerate(current_menu):
        library_match = next(
            (
                lib
                for lib in st.session_state["library"]
                if lib["id"] == today_item.get("library_id")
            ),
            None,
        )
        
        if library_match:
            display_name = library_match["name"]
        else:
            display_name = today_item.get("name", "Unknown workout")
        
        display_title = f"{index + 1}. {display_name} | {today_item['reps']} reps x {today_item['sets']} sets"

        with st.expander(display_title):
            if library_match:
                # ★変更：ここでも専用関数を使う
                display_media(library_match["url"])
                
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
    st.markdown('<div class="section-header">日々のメニューを作成</div>', unsafe_allow_html=True)

    selected_date = st.date_input("編集する日付を選択", date.today(), key="admin_date")
    date_str = selected_date.isoformat()

    available_names = [item["name"] for item in st.session_state["library"]]
    library_by_name = {item["name"]: item for item in st.session_state["library"]}
    
    current_menu = sheets_repository.get_todays_menu(date_str)
    st.caption(f"ℹ️ 現在、{date_str} には {len(current_menu)} 件のメニューが登録されています。")

    with st.form(key="add_today_form"):
        if available_names:
            selected_name = st.selectbox("Select a workout from the library", available_names)
            col1, col2 = st.columns(2)
            with col1:
                target_reps = st.text_input("Reps (e.g. 10 or 8-10)")
            with col2:
                target_sets = st.text_input("Sets (e.g. 3)")

            submit_today = st.form_submit_button(label=f"{date_str} のメニューに追加")
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
                                target_date=date_str
                            )
                            refresh_session_state_from_storage()
                            st.success(f"Added '{selected_name}' to {date_str} menu.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Failed to save: {exc}")
                else:
                    st.error("Please enter both reps and sets.")
        else:
            st.warning("Add workouts to the library first.")

    if st.button(f"{date_str} のメニューをすべて削除"):
        try:
            sheets_repository.clear_todays_menu(target_date=date_str)
            refresh_session_state_from_storage()
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to clear: {exc}")


def render_library_create_admin() -> None:
    st.markdown('<div class="section-header">Add Workout to Library</div>', unsafe_allow_html=True)
    
    new_cat = st.selectbox("Category", CATEGORIES, format_func=lambda c: CATEGORY_LABELS[c])
    new_sub_cat = ""
    if new_cat == "筋力":
        new_sub_cat = st.selectbox("部位", ["Push", "Pull", "Leg"], key="create_sub")

    with st.form(key="add_library_form"):
        new_name = st.text_input("Workout name (e.g. Pull-up)")
        
        uploaded_file = st.file_uploader("スマホの動画・写真を選択", type=["mp4", "mov", "jpg", "jpeg", "png"])
        new_url = st.text_input("またはVideo URLを直接入力 (YouTube等)")
        
        new_point = st.text_area("Coaching tip (optional)")

        submit_lib = st.form_submit_button(label="Add to library")
        if submit_lib:
            if new_name and (new_url or uploaded_file):
                if any(item["name"] == new_name for item in st.session_state["library"]):
                    st.error("That workout name already exists. Please use a different name.")
                else:
                    try:
                        final_url = new_url
                        
                        if uploaded_file is not None:
                            with st.spinner("ファイルをGoogleドライブに保存しています...（数秒かかります）"):
                                file_bytes = uploaded_file.read()
                                final_url = sheets_repository.upload_media(
                                    file_bytes=file_bytes,
                                    mime_type=uploaded_file.type,
                                    file_name=uploaded_file.name
                                )

                        save_cat = f"{new_cat}_{new_sub_cat}" if new_sub_cat else new_cat
                        
                        sheets_repository.add_library_item(
                            category=save_cat,
                            name=new_name,
                            url=final_url,
                            point=new_point,
                        )
                        refresh_session_state_from_storage()
                        st.success(f"Added '{new_name}' to the library.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Failed to register: {exc}")
            else:
                st.error("Workout name and (Video URL or File) are required.")


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

    raw_cat = target_item["category"]
    if "_" in raw_cat:
        base_cat, base_sub = raw_cat.split("_", 1)
    else:
        base_cat, base_sub = raw_cat, "Push"

    edit_cat = st.selectbox(
        "Category",
        CATEGORIES,
        index=CATEGORIES.index(base_cat) if base_cat in CATEGORIES else 0,
        format_func=lambda c: CATEGORY_LABELS[c],
        key="edit_cat_select"
    )
    
    edit_sub_cat = ""
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
elif page == "Daily Workout":
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
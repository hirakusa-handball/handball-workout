import streamlit as st

from constants import CATEGORIES
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
    st.markdown('<div class="section-header">本日のトレーニングを組む</div>', unsafe_allow_html=True)

    available_names = [item["name"] for item in st.session_state["library"]]
    library_by_name = {item["name"]: item for item in st.session_state["library"]}
    with st.form(key="add_today_form"):
        if available_names:
            selected_name = st.selectbox("ライブラリから種目を選択", available_names)
            col1, col2 = st.columns(2)
            with col1:
                target_reps = st.text_input("レップ数 (例: 10, または 8〜10)")
            with col2:
                target_sets = st.text_input("セット数 (例: 3)")

            submit_today = st.form_submit_button(label="本日のメニューに追加")
            if submit_today:
                if target_reps and target_sets:
                    selected_item = library_by_name.get(selected_name)
                    if not selected_item:
                        st.error("選択した種目が見つかりません。")
                    else:
                        try:
                            sheets_repository.add_todays_menu_item(
                                library_id=selected_item["id"],
                                reps=target_reps,
                                sets=target_sets,
                            )
                            refresh_session_state_from_storage()
                            st.success(f"「{selected_name}」を本日のメニューに追加しました。")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"保存に失敗しました: {exc}")
                else:
                    st.error("レップ数とセット数を入力してください。")
        else:
            st.warning("先にトレーニングライブラリへ種目を追加してください。")

    if st.button("本日のメニューを全てクリアする"):
        try:
            sheets_repository.clear_todays_menu()
            refresh_session_state_from_storage()
            st.rerun()
        except Exception as exc:
            st.error(f"クリアに失敗しました: {exc}")


def render_library_create_admin() -> None:
    st.markdown('<div class="section-header">ライブラリに新規種目を登録</div>', unsafe_allow_html=True)
    with st.form(key="add_library_form"):
        new_cat = st.selectbox("カテゴリー", CATEGORIES)
        new_name = st.text_input("種目名 (例: 懸垂)")
        new_url = st.text_input("参考動画URL (YouTubeリンク等)")
        new_point = st.text_area("意識ポイント (任意)")

        submit_lib = st.form_submit_button(label="ライブラリに登録")
        if submit_lib:
            if new_name and new_url:
                if any(item["name"] == new_name for item in st.session_state["library"]):
                    st.error("その種目名は既に登録されています。別の名前を指定してください。")
                else:
                    try:
                        sheets_repository.add_library_item(
                            category=new_cat,
                            name=new_name,
                            url=new_url,
                            point=new_point,
                        )
                        refresh_session_state_from_storage()
                        st.success(f"「{new_name}」をライブラリ({new_cat})に登録しました。")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"登録に失敗しました: {exc}")
            else:
                st.error("種目名と動画URLは必須です。")


def render_library_edit_admin() -> None:
    st.markdown('<div class="section-header">ライブラリの編集・削除</div>', unsafe_allow_html=True)
    available_names = [item["name"] for item in st.session_state["library"]]
    if not available_names:
        st.write("ライブラリに登録されている種目がありません。")
        return

    edit_target_name = st.selectbox(
        "編集または削除する種目を選択",
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
        st.error("対象の種目が見つかりません。")
        return
    target_item = st.session_state["library"][target_index]

    with st.form(key="edit_lib_form"):
        edit_cat = st.selectbox(
            "カテゴリー",
            CATEGORIES,
            index=CATEGORIES.index(target_item["category"]),
        )
        edit_name = st.text_input("種目名", value=target_item["name"])
        edit_url = st.text_input("参考動画URL", value=target_item["url"])
        edit_point = st.text_area("意識ポイント", value=target_item["point"])
        submit_update = st.form_submit_button("情報を更新する")

    delete_btn = st.button("この種目をライブラリから削除する")

    if submit_update:
        if edit_name and edit_url:
            conflict = any(
                item["name"] == edit_name and i != target_index
                for i, item in enumerate(st.session_state["library"])
            )
            if conflict:
                st.error("その種目名は既に他の種目で使われています。")
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
                    st.success("ライブラリの情報を更新しました。")
                    st.rerun()
                except Exception as exc:
                    st.error(f"更新に失敗しました: {exc}")
        else:
            st.error("種目名と動画URLは必須です。")

    if delete_btn:
        try:
            sheets_repository.delete_library_item(target_item["id"])
            refresh_session_state_from_storage()
            st.success(f"「{edit_target_name}」を削除しました。")
            st.rerun()
        except Exception as exc:
            st.error(f"削除に失敗しました: {exc}")

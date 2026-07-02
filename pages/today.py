import streamlit as st


def render_todays_training_page() -> None:
    st.markdown('<div class="main-title">TODAY\'S WORKOUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">本日の実行メニュー</div>', unsafe_allow_html=True)

    if not st.session_state["todays_menu"]:
        st.write("本日のメニューはまだ設定されていません。")
        return

    for index, today_item in enumerate(st.session_state["todays_menu"]):
        library_match = next(
            (lib for lib in st.session_state["library"] if lib["name"] == today_item["name"]),
            None,
        )
        display_title = f"{index + 1}. {today_item['name']} | {today_item['reps']}回 × {today_item['sets']}セット"

        with st.expander(display_title):
            if library_match:
                st.video(library_match["url"])
                if library_match["point"]:
                    st.caption(f"ポイント: {library_match['point']}")
            else:
                st.error("※ライブラリから元のデータが削除されています。")

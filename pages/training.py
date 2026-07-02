import streamlit as st

from constants import CATEGORIES


def render_training_page() -> None:
    st.markdown('<div class="main-title">TRAINING LIBRARY</div>', unsafe_allow_html=True)
    st.write("チームの全トレーニングメニューの蓄積です。")

    tabs = st.tabs(CATEGORIES)
    for i, cat in enumerate(CATEGORIES):
        with tabs[i]:
            st.markdown(f'<div class="section-header">{cat}メニュー</div>', unsafe_allow_html=True)
            cat_items = [item for item in st.session_state["library"] if item["category"] == cat]

            if not cat_items:
                st.caption("このカテゴリーにはまだメニューが登録されていません。")
                continue

            for item in cat_items:
                with st.expander(item["name"]):
                    st.video(item["url"])
                    if item["point"]:
                        st.caption(f"ポイント: {item['point']}")

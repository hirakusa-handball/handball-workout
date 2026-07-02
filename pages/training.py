import streamlit as st

from constants import CATEGORIES, CATEGORY_LABELS


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
            cat_items = [item for item in st.session_state["library"] if item["category"] == cat]

            if not cat_items:
                st.caption("No exercises registered in this category yet.")
                continue

            for item in cat_items:
                with st.expander(item["name"]):
                    st.video(item["url"])
                    if item["point"]:
                        st.caption(f"Tip: {item['point']}")

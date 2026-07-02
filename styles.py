import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            font-family: 'Yu Mincho', 'Hiragino Mincho ProN', 'Noto Serif JP', serif !important;
            letter-spacing: 0.05em;
        }
        .main-title {
            font-size: 28px;
            font-weight: 300;
            text-align: center;
            color: #333333;
            margin-top: 20px;
            margin-bottom: 40px;
            letter-spacing: 0.15em;
        }
        .section-header {
            font-size: 20px;
            font-weight: 400;
            color: #333333;
            border-bottom: 1px solid #BFA77F;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
            letter-spacing: 0.1em;
        }
        .target-box {
            color: #8C7B5D;
            font-size: 14px;
            font-weight: normal;
            margin-bottom: 15px;
            border-left: 2px solid #BFA77F;
            padding-left: 10px;
        }
        @media (prefers-color-scheme: dark) {
            .main-title, .section-header { color: #EEEEEE; }
            .section-header { border-bottom: 1px solid #8C7B5D; }
            .target-box { color: #D4C8B8; border-left: 2px solid #D4C8B8; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

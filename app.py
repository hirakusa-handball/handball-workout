import streamlit as st

# 1. ページ全体の設定
st.set_page_config(page_title="Handball Team Hub", layout="centered")

# 2. カスタムCSS（画像の雰囲気に合わせた和モダン・ミニマルデザイン）
st.markdown("""
    <style>
    /* 研ぎ澄まされた明朝体フォント */
    html, body, [class*="css"] {
        font-family: 'Yu Mincho', 'Hiragino Mincho ProN', 'Noto Serif JP', serif !important;
        letter-spacing: 0.05em;
    }
    
    /* メインタイトル */
    .main-title {
        font-size: 28px;
        font-weight: 300;
        text-align: center;
        color: #333333;
        margin-top: 20px;
        margin-bottom: 40px;
        letter-spacing: 0.15em;
    }
    
    /* セクションヘッダー（細い下線で上品に） */
    .section-header {
        font-size: 20px;
        font-weight: 400;
        color: #333333;
        border-bottom: 1px solid #BFA77F; /* 画像にあるような落ち着いたベージュ/ゴールド */
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
        letter-spacing: 0.1em;
    }
    
    /* 推奨回数の表示（控えめなアクセントライン） */
    .target-box {
        color: #8C7B5D;
        font-size: 14px;
        font-weight: normal;
        margin-bottom: 15px;
        border-left: 2px solid #BFA77F;
        padding-left: 10px;
    }
    
    /* ダークモード時の自動調整 */
    @media (prefers-color-scheme: dark) {
        .main-title, .section-header { color: #EEEEEE; }
        .section-header { border-bottom: 1px solid #8C7B5D; }
        .target-box { color: #D4C8B8; border-left: 2px solid #D4C8B8; }
    }
    </style>
""", unsafe_allow_html=True)

# 3. サイドバー
st.sidebar.title("メニュー")
page = st.sidebar.radio("ページを選択", ["フィジカル", "戦術・データ分析"])

# ==========================================
# ページA: フィジカル
# ==========================================
if page == "フィジカル":
    st.markdown('<div class="main-title">HANDBALL WORKOUT</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["筋力", "瞬発力", "競技特化", "体幹", "本日のメニュー"])

    with tab1:
        st.markdown('<div class="section-header">筋力・筋肥大</div>', unsafe_allow_html=True)
        st.caption("コンタクトに負けない体格と、基礎出力の向上。")
        
        push_tab, pull_tab, leg_tab = st.tabs(["押す", "引く", "下半身"])
        
        with push_tab:
            with st.expander("ベンチプレス"):
                st.markdown('<div class="target-box">目標: 8〜10回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=vthMCtgVtFw")
                st.caption("ポイント: 肩甲骨を寄せて胸を張り、バーを下ろす位置を意識する。")
                
        with pull_tab:
            with st.expander("懸垂"):
                st.markdown('<div class="target-box">目標: 10回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=vthMCtgVtFw")
                st.caption("ポイント: 反動を使わず、背中の筋肉で引くことを意識する。")
                
        with leg_tab:
            with st.expander("バックスクワット"):
                st.markdown('<div class="target-box">目標: 10回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=U3HhmJEFAZw")
                st.caption("ポイント: 膝が内側に入らないように注意し、深くしゃがむ。")
                
            with st.expander("デッドリフト"):
                st.markdown('<div class="target-box">目標: 5〜8回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=op9kVnSso6Q")
                st.caption("ポイント: 背中が丸まらないように、股関節から動かすヒンジ動作を意識する。")

    with tab2:
        st.markdown('<div class="section-header">瞬発力</div>', unsafe_allow_html=True)
        with st.expander("ハングクリーン"):
            st.markdown('<div class="target-box">目標: 3〜5回 × 3セット</div>', unsafe_allow_html=True)
            st.video("clean.mp4")
            st.caption("ポイント: 腕で引くのではなく、股関節の爆発的な進展でバーを跳ね上げる。")

    with tab3:
        st.markdown('<div class="section-header">競技特化</div>', unsafe_allow_html=True)
        with st.expander("ブルガリアンスクワット"):
            st.markdown('<div class="target-box">目標: 左右 各10回 × 3セット</div>', unsafe_allow_html=True)
            st.video("https://www.youtube.com/watch?v=2C-uNgKwPLE")
            st.caption("ポイント: 前足の踵で地面を踏み込み、お尻の筋肉を使うことを意識する。")

    with tab4:
        st.markdown('<div class="section-header">体幹</div>', unsafe_allow_html=True)
        with st.expander("ロシアンツイスト"):
            st.markdown('<div class="target-box">目標: 20回 × 3セット</div>', unsafe_allow_html=True)
            st.video("https://www.youtube.com/watch?v=wkD8rjkodUI")
            st.caption("ポイント: 足を浮かせてバランスを取りながら、お腹をしっかり捻る。")

    with tab5:
        st.markdown('<div class="section-header">本日のトレーニング</div>', unsafe_allow_html=True)
        with st.expander("ベンチプレス | 8〜10回 × 3セット"):
            st.video("https://www.youtube.com/watch?v=vthMCtgVtFw")
            
        with st.expander("バックスクワット | 10回 × 3セット"):
            st.video("https://www.youtube.com/watch?v=U3HhmJEFAZw")
            
        with st.expander("デッドリフト | 5〜8回 × 3セット"):
            st.video("https://www.youtube.com/watch?v=op9kVnSso6Q")

# ==========================================
# ページB: 分析
# ==========================================
elif page == "戦術・データ分析":
    st.markdown('<div class="main-title">HANDBALL ANALYSIS</div>', unsafe_allow_html=True)
    
    tab_of, tab_df = st.tabs(["オフェンス", "ディフェンス"])
    
    with tab_of:
        st.markdown('<div class="section-header">オフェンス戦術</div>', unsafe_allow_html=True)
        
        st.write("直近のポジション別 シュート決定率")
        st.bar_chart({
            "6m": 75,
            "9m": 42,
            "ウイング": 58,
            "7mスロー": 80,
            "速攻": 88
        })
        
        st.divider()
        
        with st.expander("基本のクロスプレー"):
            st.write("きっかけの動きとタイミングの確認。")
            st.video("https://www.youtube.com/watch?v=dummy_url_1")
            
        with st.expander("数的優位（6対5）の攻め方"):
            st.write("退場者が出た際の確実な崩し方のセオリー。")
            st.video("https://www.youtube.com/watch?v=dummy_url_2")

    with tab_df:
        st.markdown('<div class="section-header">ディフェンスシステム</div>', unsafe_allow_html=True)
        
        with st.expander("基本の 0-6 ディフェンス"):
            st.write("隣との間隔を埋め、ポストを完全に抑える動きの徹底。")
            st.video("https://www.youtube.com/watch?v=dummy_url_3")
            
        with st.expander("牽制を入れた 1-5 ディフェンス"):
            st.write("相手エースに対するトップの当たり方とカバーリング。")
            st.video("https://www.youtube.com/watch?v=dummy_url_4")

import streamlit as st

# 1. ページ全体の設定（※必ず最初に書く）
st.set_page_config(page_title="Handball Team Hub", layout="centered")

# 2. カスタムCSS（共通デザイン）
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif !important;
    }
    .main-title {
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        color: #242B35;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .catchphrase {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        color: #555555;
        margin-bottom: 25px;
        border-bottom: 2px dashed #999999;
        padding-bottom: 15px;
    }
    .section-header {
        background-color: #242B35;
        color: #FFFFFF !important;
        padding: 8px 15px;
        font-size: 18px;
        font-weight: bold;
        border-left: 6px solid #C93A22;
        margin-top: 20px;
        margin-bottom: 15px;
        display: inline-block;
        width: 100%;
    }
    .target-box {
        background-color: #B39A51;
        color: #FFFFFF;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: bold;
        margin-bottom: 10px;
        border-radius: 2px;
        display: inline-block;
    }
    @media (prefers-color-scheme: dark) {
        .main-title { color: #FFFFFF; }
        .catchphrase { color: #AAAAAA; border-bottom: 2px dashed #555555; }
    }
    </style>
""", unsafe_allow_html=True)

# 3. サイドバーでページを切り替える設定
st.sidebar.title("🤾 メニュー")
page = st.sidebar.radio("ページを選択してください", ["🏋️ フィジカル", "📊 戦術・データ分析"])

# ==========================================
# ページA: フィジカル（これまでの内容）
# ==========================================
if page == "🏋️ フィジカル":
    st.markdown('<div class="main-title">HANDBALL<br><span style="font-size: 24px;">WORKOUT</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="catchphrase">試合で当たり負けして、どうするの？<br>チーム専用・目的別プログラム</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["筋力・筋肥大", "瞬発力", "競技特化", "体幹", "今日のメニュー"])

    with tab1:
        st.markdown('<div class="section-header">筋力・筋肥大（土台作り）</div>', unsafe_allow_html=True)
        push_tab, pull_tab, leg_tab = st.tabs(["押す (Push)", "引く (Pull)", "下半身 (Leg)"])
        with push_tab:
            with st.expander("ベンチプレス"):
                st.markdown('<div class="target-box">目標: 8〜10回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=vthMCtgVtFw")
        with pull_tab:
            with st.expander("懸垂（チンニング）"):
                st.markdown('<div class="target-box">目標: 10回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=vthMCtgVtFw") # 仮のURL
        with leg_tab:
            with st.expander("バックスクワット"):
                st.markdown('<div class="target-box">目標: 10回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=U3HhmJEFAZw")
            with st.expander("デッドリフト"):
                st.markdown('<div class="target-box">目標: 5〜8回 × 3セット</div>', unsafe_allow_html=True)
                st.video("https://www.youtube.com/watch?v=op9kVnSso6Q")

    with tab2:
        st.markdown('<div class="section-header">瞬発系メニュー</div>', unsafe_allow_html=True)
        with st.expander("ハングクリーン"):
            st.markdown('<div class="target-box">目標: 3〜5回 × 3セット</div>', unsafe_allow_html=True)
            st.video("clean.mp4") # 仮のファイル

    with tab3:
        st.markdown('<div class="section-header">競技特化メニュー</div>', unsafe_allow_html=True)
        with st.expander("ブルガリアンスクワット"):
            st.markdown('<div class="target-box">目標: 左右 各10回 × 3セット</div>', unsafe_allow_html=True)
            st.video("https://www.youtube.com/watch?v=2C-uNgKwPLE")

    with tab4:
        st.markdown('<div class="section-header">体幹（コア）メニュー</div>', unsafe_allow_html=True)
        with st.expander("ロシアンツイスト"):
            st.markdown('<div class="target-box">目標: 20回 × 3セット</div>', unsafe_allow_html=True)
            st.video("https://www.youtube.com/watch?v=wkD8rjkodUI")

    with tab5:
        st.markdown('<div class="section-header">本日のトレーニング</div>', unsafe_allow_html=True)
        with st.expander("ベンチプレス | 8〜10回 × 3セット"):
            st.video("https://www.youtube.com/watch?v=vthMCtgVtFw")
        with st.expander("バックスクワット | 10回 × 3セット"):
            st.video("https://www.youtube.com/watch?v=U3HhmJEFAZw")
        with st.expander("デッドリフト | 5〜8回 × 3セット"):
            st.video("https://www.youtube.com/watch?v=op9kVnSso6Q")

# ==========================================
# ページB: 分析（新規追加）
# ==========================================
elif page == "📊 戦術・データ分析":
    st.markdown('<div class="main-title">HANDBALL<br><span style="font-size: 24px;">ANALYSIS</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="catchphrase">戦術を理解し、試合を支配する<br>チーム専用・戦術分析ボード</div>', unsafe_allow_html=True)
    
    # OFとDFのタブを作成
    tab_of, tab_df = st.tabs(["⚔️ OF (オフェンス)", "🛡️ DF (ディフェンス)"])
    
    with tab_of:
        st.markdown('<div class="section-header">オフェンス戦術・スタッツ</div>', unsafe_allow_html=True)
        
        # スタッツの可視化（簡易的なデータグラフ）
        st.write("📈 **直近のポジション別 シュート決定率**")
        st.bar_chart({
            "6m (ポスト)": 75,
            "9m (ロング)": 42,
            "ウイング (サイド)": 58,
            "7mスロー": 80,
            "速攻": 88
        })
        
        st.divider()
        st.write("🎬 **戦術ビデオ・フォーメーション**")
        
        with st.expander("基本のクロスプレー（きっかけ）"):
            st.write("ここに戦術解説のテキストや、動きのポイントを書きます。")
            st.video("https://www.youtube.com/watch?v=dummy_url_1") # 後で戦術動画に差し替え
            
        with st.expander("数的優位（6対5）の攻め方"):
            st.write("退場者が出た際の確実な崩し方についての解説。")
            st.video("https://www.youtube.com/watch?v=dummy_url_2") # 後で戦術動画に差し替え

    with tab_df:
        st.markdown('<div class="section-header">ディフェンスシステム</div>', unsafe_allow_html=True)
        
        st.write("🎬 **システム別解説**")
        with st.expander("基本の 0-6 ディフェンス"):
            st.write("隣との間隔を埋め、ポストを完全に抑える動きの徹底。")
            st.video("https://www.youtube.com/watch?v=dummy_url_3") # 後で戦術動画に差し替え
            
        with st.expander("牽制を入れた 1-5 ディフェンス"):
            st.write("相手のエースを潰すためのトップの当たり方と、残りの5人のカバーリング。")
            st.video("https://www.youtube.com/watch?v=dummy_url_4") # 後で戦術動画に差し替え

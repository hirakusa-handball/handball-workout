import streamlit as st

# 1. ページ全体の設定
st.set_page_config(page_title="Handball Physical", layout="centered")

# 2. 画像のデザイン（和風モダン×フィットネス）を再現するCSS
st.markdown("""
    <style>
    /* 日本語フォントを太く力強いゴシック体に統一 */
    html, body, [class*="css"] {
        font-family: 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif !important;
    }
    
    /* メインタイトル */
    .main-title {
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        color: #242B35; /* 画像のネイビーブルー */
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    
    /* キャッチコピー（画像の点線デザインをリスペクト） */
    .catchphrase {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        color: #555555;
        margin-bottom: 25px;
        border-bottom: 2px dashed #999999;
        padding-bottom: 15px;
    }
    
    /* セクションのヘッダー（画像の四角いロゴブロック風） */
    .section-header {
        background-color: #242B35; /* ネイビー */
        color: #FFFFFF !important;
        padding: 8px 15px;
        font-size: 18px;
        font-weight: bold;
        border-left: 6px solid #C93A22; /* 画像の赤色アクセント */
        margin-top: 20px;
        margin-bottom: 15px;
        display: inline-block;
        width: 100%;
    }
    
    /* 推奨回数ボックス（画像の「ご入会・体験」ボタンのマスタードイエロー） */
    .target-box {
        background-color: #B39A51; /* マスタードイエロー */
        color: #FFFFFF;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: bold;
        margin-bottom: 10px;
        border-radius: 2px;
        display: inline-block;
    }
    
    /* ダークモード時の自動調整 */
    @media (prefers-color-scheme: dark) {
        .main-title { color: #FFFFFF; }
        .catchphrase { color: #AAAAAA; border-bottom: 2px dashed #555555; }
    }
    </style>
""", unsafe_allow_html=True)

# 3. ヘッダー
st.markdown('<div class="main-title">UTokyo Handball Team<br>HANDBALL WORKOUT</div>', unsafe_allow_html=True)

# 4. メインタブ（日本語表記に変更）
tab1, tab2, tab3, tab4, tab5 = st.tabs(["筋力・筋肥大", "瞬発力", "競技特化", "体幹", "今日のメニュー"])

# --- タブ1: 筋力 ---
with tab1:
    st.markdown('<div class="section-header">筋力・筋肥大（土台作り）</div>', unsafe_allow_html=True)
    st.write("コンタクトに負けない体格と、基礎出力の向上を目指します。")
    
    push_tab, pull_tab, leg_tab = st.tabs(["押す (Push)", "引く (Pull)", "下半身 (Leg)"])
    
    with push_tab:
        st.markdown("#### ベンチプレス")
        st.markdown('<div class="target-box">目標: 8〜10回 × 3セット</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=vthMCtgVtFw") 
        
    with pull_tab:
        st.markdown("#### 背中・二頭系メニュー")
        st.caption("※メニュー準備中")

    　　　st.markdown("#### 懸垂（チンニング）")
        st.markdown('<div class="target-box">目標: 10回 × 3セット</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=実際の動画のID") 
        st.divider()
    with leg_tab:
        st.markdown("#### バックスクワット")
        st.markdown('<div class="target-box">目標: 10回 × 3セット</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=U3HhmJEFAZw")
        st.divider()
        
        st.markdown("#### デッドリフト")
        st.markdown('<div class="target-box">目標: 5〜8回 × 3セット</div>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=op9kVnSso6Q")

# --- タブ2: 瞬発 ---
with tab2:
    st.markdown('<div class="section-header">瞬発系メニュー</div>', unsafe_allow_html=True)
    st.write("作った筋肉を「一瞬で爆発させる」力へ変換します。")
    
    st.markdown("#### ハングクリーン")
    st.markdown('<div class="target-box">目標: 3〜5回 × 3セット</div>', unsafe_allow_html=True)
    st.video("clean.mp4") 

# --- タブ3: 競技特化 ---
with tab3:
    st.markdown('<div class="section-header">競技特化メニュー</div>', unsafe_allow_html=True)
    st.write("片足での踏み切りや、空中でのボディコントロールを強化します。")
    
    st.markdown("#### ブルガリアンスクワット")
    st.markdown('<div class="target-box">目標: 左右 各10回 × 3セット</div>', unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=2C-uNgKwPLE")

# --- タブ4: 体幹 ---
with tab4:
    st.markdown('<div class="section-header">体幹（コア）メニュー</div>', unsafe_allow_html=True)
    st.write("空中での姿勢維持、シュート時の捻り動作の安定を作ります。")
    
    st.markdown("#### ロシアンツイスト")
    st.markdown('<div class="target-box">目標: 20回 × 3セット</div>', unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=wkD8rjkodUI")
   
    st.markdown("#### バーベルバカ腹筋")
    st.markdown('<div class="target-box">目標: 10回 × 3セット</div>', unsafe_allow_html=True)
    st.divider()

# --- タブ5: 今日のメニュー ---
with tab5:
    st.markdown('<div class="section-header">本日のトレーニング</div>', unsafe_allow_html=True)
    st.write("BIG3（全身強化）プログラム")
    
    with st.expander("ベンチプレス | 8〜10回 × 3セット"):
        st.video("https://www.youtube.com/watch?v=vthMCtgVtFw")
        st.caption("ポイント: 肩甲骨を寄せて胸を張り、バーを下ろす位置を意識する。")
        
    with st.expander("バックスクワット | 10回 × 3セット"):
        st.video("https://www.youtube.com/watch?v=U3HhmJEFAZw")
        st.caption("ポイント: 膝が内側に入らないように注意し、深くしゃがむ。")
        
    with st.expander("デッドリフト | 5〜8回 × 3セット"):
        st.video("https://www.youtube.com/watch?v=op9kVnSso6Q")
        st.caption("ポイント: 背中が丸まらないように、股関節から動かすヒンジ動作を意識する。")

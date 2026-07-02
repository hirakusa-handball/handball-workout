import streamlit as st

# 1. ページ全体の設定
st.set_page_config(page_title="Handball Team Hub", layout="centered")

# 2. カスタムCSS（和モダンデザインをキープ）
st.markdown("""
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
""", unsafe_allow_html=True)

# 3. データの初期化（アプリ起動時にデフォルトのメニューをセット）
if 'todays_menu' not in st.session_state:
    st.session_state['todays_menu'] = [
        {"name": "ベンチプレス | 8〜10回 × 3セット", "url": "https://www.youtube.com/watch?v=vthMCtgVtFw", "point": "肩甲骨を寄せて胸を張り、バーを下ろす位置を意識する。"},
        {"name": "バックスクワット | 10回 × 3セット", "url": "https://www.youtube.com/watch?v=U3HhmJEFAZw", "point": "膝が内側に入らないように注意し、深くしゃがむ。"},
        {"name": "デッドリフト | 5〜8回 × 3セット", "url": "https://www.youtube.com/watch?v=op9kVnSso6Q", "point": "背中が丸まらないように、ヒンジ動作を意識する。"}
    ]

# 4. サイドバー
st.sidebar.title("メニュー")
page = st.sidebar.radio("ページを選択", ["フィジカル", "戦術・データ分析", "⚙️ 管理者設定"])

# ==========================================
# ページA: フィジカル
# ==========================================
if page == "フィジカル":
    st.markdown('<div class="main-title">HANDBALL WORKOUT</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["筋力", "瞬発力", "競技特化", "体幹", "本日のメニュー"])

    # （※タブ1〜4は長くなるため省略せず、以前のまま簡略化して記載しています）
    with tab1:
        st.write("※筋力メニューエリア")
    with tab2:
        st.write("※瞬発力メニューエリア")
    with tab3:
        st.write("※競技特化メニューエリア")
    with tab4:
        st.write("※体幹メニューエリア")

    # 動的に生成される「本日のメニュー」
    with tab5:
        st.markdown('<div class="section-header">本日のトレーニング</div>', unsafe_allow_html=True)
        
        # session_stateに保存されたデータをループ処理で全て表示
        for i, item in enumerate(st.session_state['todays_menu']):
            with st.expander(item["name"]):
                st.video(item["url"])
                if item["point"]:
                    st.caption(f"ポイント: {item['point']}")

# ==========================================
# ページB: 分析（前回と同じ）
# ==========================================
elif page == "戦術・データ分析":
    st.markdown('<div class="main-title">HANDBALL ANALYSIS</div>', unsafe_allow_html=True)
    st.write("※分析ページの内容")

# ==========================================
# ページC: 管理者設定（新規追加）
# ==========================================
elif page == "⚙️ 管理者設定":
    st.markdown('<div class="main-title">ADMINISTRATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">本日のメニュー 追加</div>', unsafe_allow_html=True)
    
    st.write("アプリ上から直接トレーニングメニューを追加できます。")
    
    # メニュー追加用の入力フォーム
    with st.form(key="add_menu_form"):
        new_name = st.text_input("種目名と回数 (例: 懸垂 | 10回 × 3セット)")
        new_url = st.text_input("動画のURL (YouTubeのリンク等)")
        new_point = st.text_area("意識するポイント (任意)")
        
        submit_button = st.form_submit_button(label="リストに追加する")
        
        # 追加ボタンが押された時の処理
        if submit_button:
            if new_name and new_url:
                # 新しいデータをリストに追加
                st.session_state['todays_menu'].append({
                    "name": new_name, 
                    "url": new_url, 
                    "point": new_point
                })
                st.success(f"「{new_name}」を追加しました！『フィジカル』タブの『本日のメニュー』を確認してください。")
            else:
                st.error("種目名と動画URLは必須です。")

    st.divider()
    
    # 現在の登録リストの確認・リセット機能
    st.markdown('<div class="section-header">現在の登録リスト</div>', unsafe_allow_html=True)
    for item in st.session_state['todays_menu']:
        st.write(f"・ {item['name']}")
    
    if st.button("メニューを全てリセット（消去）する"):
        st.session_state['todays_menu'] = []
        st.rerun()

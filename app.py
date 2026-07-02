import streamlit as st

# ==========================================
# 1. ページ設定とデザイン（CSS）
# ==========================================
st.set_page_config(page_title="Handball Team Hub", layout="centered")

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

# ==========================================
# 2. データの初期化（ライブラリと本日のメニュー）
# ==========================================
# ① トレーニングライブラリ（全種目の蓄積）
if 'library' not in st.session_state:
    st.session_state['library'] = [
        {"category": "筋力", "name": "ベンチプレス", "url": "https://www.youtube.com/watch?v=vthMCtgVtFw", "point": "肩甲骨を寄せて胸を張る。"},
        {"category": "筋力", "name": "バックスクワット", "url": "https://www.youtube.com/watch?v=U3HhmJEFAZw", "point": "膝が内側に入らないように注意。"},
        {"category": "瞬発力", "name": "ハングクリーン", "url": "clean.mp4", "point": "股関節の爆発的な進展でバーを跳ね上げる。"},
        {"category": "競技特化", "name": "ブルガリアンスクワット", "url": "https://www.youtube.com/watch?v=2C-uNgKwPLE", "point": "前足の踵で地面を踏み込む。"},
        {"category": "体幹", "name": "ロシアンツイスト", "url": "https://www.youtube.com/watch?v=wkD8rjkodUI", "point": "お腹をしっかり捻る。"}
    ]

# ② 本日のトレーニング（ライブラリから選んだもの＋レップ数・セット数）
if 'todays_menu' not in st.session_state:
    st.session_state['todays_menu'] = [
        {"name": "ベンチプレス", "reps": "10", "sets": "3"},
        {"name": "バックスクワット", "reps": "10", "sets": "3"}
    ]

# ==========================================
# 3. サイドバーナビゲーション
# ==========================================
st.sidebar.title("メニュー")
page = st.sidebar.radio("ページを選択", ["📚 トレーニング", "🔥 本日のトレーニング", "⚙️ 管理者"])

# ==========================================
# ページA: トレーニング（ライブラリ）
# ==========================================
if page == "📚 トレーニング":
    st.markdown('<div class="main-title">TRAINING LIBRARY</div>', unsafe_allow_html=True)
    st.write("チームの全トレーニングメニューの蓄積です。")
    
    categories = ["筋力", "瞬発力", "競技特化", "体幹"]
    tabs = st.tabs(categories)
    
    for i, cat in enumerate(categories):
        with tabs[i]:
            st.markdown(f'<div class="section-header">{cat}メニュー</div>', unsafe_allow_html=True)
            
            # 該当カテゴリーのメニューだけを抽出して表示
            cat_items = [item for item in st.session_state['library'] if item['category'] == cat]
            
            if not cat_items:
                st.caption("このカテゴリーにはまだメニューが登録されていません。")
            else:
                for item in cat_items:
                    with st.expander(item["name"]):
                        st.video(item["url"])
                        if item["point"]:
                            st.caption(f"ポイント: {item['point']}")

# ==========================================
# ページB: 本日のトレーニング
# ==========================================
elif page == "🔥 本日のトレーニング":
    st.markdown('<div class="main-title">TODAY\'S WORKOUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">本日の実行メニュー</div>', unsafe_allow_html=True)
    
    if not st.session_state['todays_menu']:
        st.write("本日のメニューはまだ設定されていません。")
    else:
        for index, today_item in enumerate(st.session_state['todays_menu']):
            # ライブラリから詳細情報（URLやポイント）を名前で検索して取得
            library_match = next((lib for lib in st.session_state['library'] if lib["name"] == today_item["name"]), None)
            
            # メニュー名と指定されたレップ数・セット数を表示
            display_title = f"{index + 1}. {today_item['name']} | {today_item['reps']}回 × {today_item['sets']}セット"
            
            with st.expander(display_title):
                if library_match:
                    st.video(library_match["url"])
                    if library_match["point"]:
                        st.caption(f"ポイント: {library_match['point']}")
                else:
                    st.error("※ライブラリから元のデータが削除されています。")

# ==========================================
# ページC: 管理者
# ==========================================
elif page == "⚙️ 管理者":
    st.markdown('<div class="main-title">ADMINISTRATION</div>', unsafe_allow_html=True)
    
    # ----------------------------------------
    # 管理機能①：本日のトレーニング設定
    # ----------------------------------------
    st.markdown('<div class="section-header">🔥 本日のトレーニングを組む</div>', unsafe_allow_html=True)
    st.write("ライブラリから種目を選び、今日のメニューに追加します。")
    
    # ライブラリに登録されている種目名だけをリスト化
    available_names = [item["name"] for item in st.session_state['library']]
    
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
                    st.session_state['todays_menu'].append({
                        "name": selected_name,
                        "reps": target_reps,
                        "sets": target_sets
                    })
                    st.success(f"「{selected_name}」を本日のメニューに追加しました！")
                else:
                    st.error("レップ数とセット数を入力してください。")
        else:
            st.warning("先にトレーニングライブラリへ種目を追加してください。")
            
    # 本日のメニューのリセットボタン
    if st.button("本日のメニューを全てクリアする"):
        st.session_state['todays_menu'] = []
        st.rerun()

    st.divider()

    # ----------------------------------------
    # 管理機能②：トレーニングライブラリへの追加
    # ----------------------------------------
    st.markdown('<div class="section-header">📚 ライブラリに新規種目を登録</div>', unsafe_allow_html=True)
    st.write("新しいトレーニング種目をデータベースに蓄積します。")
    
    with st.form(key="add_library_form"):
        new_cat = st.selectbox("カテゴリー", ["筋力", "瞬発力", "競技特化", "体幹"])
        new_name = st.text_input("種目名 (例: 懸垂)")
        new_url = st.text_input("参考動画URL (YouTubeリンク等)")
        new_point = st.text_area("意識ポイント (任意)")
        
        submit_lib = st.form_submit_button(label="ライブラリに登録")
        
        if submit_lib:
            if new_name and new_url:
                # 既に同じ名前の種目がないかチェック
                if any(item['name'] == new_name for item in st.session_state['library']):
                    st.error("その種目名は既に登録されています。別の名前を指定してください。")
                else:
                    st.session_state['library'].append({
                        "category": new_cat,
                        "name": new_name,
                        "url": new_url,
                        "point": new_point
                    })
                    st.success(f"「{new_name}」をライブラリ({new_cat})に登録しました！")
            else:
                st.error("種目名と動画URLは必須です。")

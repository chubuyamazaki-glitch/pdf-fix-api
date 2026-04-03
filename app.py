import streamlit as st
import gspread
from google.oauth2 import service_account

# --- スプレッドシートからユーザー名を取得する関数 ---
def get_user_list():
    info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(info)
    scoped_creds = creds.with_scopes([
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets'
    ])
    gc = gspread.authorize(scoped_creds)
    
    # スプレッドシートを開く
    sh = gc.open_by_key(SS_ID)
    try:
        # 「ユーザーマスタ」シートを選択
        user_sheet = sh.worksheet("ユーザーマスタ")
        # 全データ取得（1列目が名前と想定）
        data = user_sheet.get_all_values()
        # ヘッダーを除いたリストを作成
        return [row[1] for row in data[1:] if row[1]] 
    except:
        return ["名前を手入力してください"]

# --- 画面部分の書き換え ---
user_options = get_user_list()
user_name = st.selectbox("申請者を選択してください", user_options)

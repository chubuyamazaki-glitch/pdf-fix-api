import streamlit as st
import fitz
import io
import base64

st.set_page_config(page_title="PDF Fix API")

def process_pdf(pdf_bytes):
    src_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    new_doc = fitz.open()
    target_width, target_height = 1191, 842
    for page in src_doc:
        zoom = 3.5 
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        new_page = new_doc.new_page(width=target_width, height=target_height)
        img_bytes = pix.tobytes("png")
        new_page.insert_image(new_page.rect, stream=img_bytes)
    output_stream = io.BytesIO()
    new_doc.save(output_stream, garbage=3, deflate=True)
    return output_stream.getvalue()

# URLパラメータ取得
query_params = st.query_params

# GASからの自動アクセス(mode=api)の場合
if query_params.get("mode") == "api":
    # 画面には何も出さず、受け取ったデータを処理して code タグで出力する
    # ※GASの UrlFetchApp.fetch の payload を取得
    st.write("Processing...") # 処理中フラグ
    
    # 簡易的に、もしPOSTデータがあれば処理するロジック（実際にはStreamlitの仕様に合わせる）
    # 手動用ではないため、隠し入力フィールドなどは置かずにレスポンスを待つ
    # (ここは今のところ、手動変換での動作を優先しつつAPI口を確保しています)

# 通常の画面表示
st.title("PDF座標補正ツール (高画質)")
uploaded_file = st.file_uploader("PDFを選択", type="pdf")
if uploaded_file:
    fixed_data = process_pdf(uploaded_file.read())
    st.download_button("修正済みPDFをダウンロード", fixed_data, "fixed.pdf", "application/pdf")

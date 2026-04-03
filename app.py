import streamlit as st
import fitz
import io
import base64

# ページ設定
st.set_page_config(page_title="PDF Fix API", layout="wide")

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

# --- APIモード判定 ---
# URLパラメータ ?mode=api&data=... を取得
query_params = st.query_params

if query_params.get("mode") == "api":
    # URLまたはPOSTデータから取得
    api_data = query_params.get("data")
    
    # 万が一URLに乗らない場合に備え、画面上の入力欄も監視
    if not api_data:
        api_data = st.text_area("data", label_visibility="collapsed")

    if api_data:
        try:
            # データのクリーニング（余計なスペースなどを消す）
            clean_data = api_data.strip()
            fixed_pdf = process_pdf(base64.b64decode(clean_data))
            # GASが抜き出しやすいように <code> で出力
            st.code(base64.b64encode(fixed_pdf).decode("utf-8"))
            st.stop()
        except Exception as e:
            st.write(f"Error: {e}")

# 通常画面（手動用）
st.title("PDF座標補正ツール (高画質)")
uploaded_file = st.file_uploader("手動変換用", type="pdf")
if uploaded_file:
    fixed_data = process_pdf(uploaded_file.read())
    st.download_button("修正済みPDFをダウンロード", fixed_data, "fixed.pdf", "application/pdf")

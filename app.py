import streamlit as st
import fitz  # PyMuPDF
import io

st.title("PDF座標補正API (軽量版)")

uploaded_file = st.file_uploader("PDFを選択", type="pdf")

if uploaded_file:
    src_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    new_doc = fitz.open()
    
    # A3横サイズ
    target_width, target_height = 1191, 842
    
    for page in src_doc:
        # 【修正ポイント1】解像度を3倍→2倍に少し落とす（これだけでサイズは半分以下になります）
        zoom = 2 
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        
        new_page = new_doc.new_page(width=target_width, height=target_height)
        
        # 【修正ポイント2】画像をJPEG形式で、かつ品質を調整して圧縮する
        # pngよりもjpgの方が圧倒的に軽くなります
        img_bytes = pix.tobytes("jpg", jpg_quality=75) 
        
        new_page.insert_image(new_page.rect, stream=img_bytes)
    
    output_stream = io.BytesIO()
    # 【修正ポイント3】PDF保存時にもガベージコレクション（不要データ削除）を実行
    new_doc.save(output_stream, garbage=4, deflate=True)
    
    st.download_button(
        label="修正済みPDFをダウンロード",
        data=output_stream.getvalue(),
        file_name="fixed_standard_light.pdf",
        mime="application/pdf"
    )

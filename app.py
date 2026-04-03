import streamlit as st
import fitz  # PyMuPDF
import io

st.title("PDF座標補正API (高画質版)")

uploaded_file = st.file_uploader("PDFを選択", type="pdf")

if uploaded_file:
    src_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    new_doc = fitz.open()
    
    # A3横サイズ (ポイント単位)
    target_width, target_height = 1191, 842
    
    for page in src_doc:
        # 【調整ポイント1】解像度を 3.5倍 に設定
        # これにより文字の輪郭が非常にシャープになります
        zoom = 3.5 
        mat = fitz.Matrix(zoom, zoom)
        
        # 【調整ポイント2】PNG形式に戻す
        # JPGよりもファイルサイズは増えますが、文字の可読性が圧倒的に上がります
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        
        new_page = new_doc.new_page(width=target_width, height=target_height)
        
        # 1枚の「絵」としてA3枠にピッタリ貼り付け
        img_bytes = pix.tobytes("png")
        new_page.insert_image(new_page.rect, stream=img_bytes)
    
    output_stream = io.BytesIO()
    # 保存時の圧縮オプションを最適化
    new_doc.save(output_stream, garbage=3, deflate=True)
    
    st.download_button(
        label="高画質PDFをダウンロード",
        data=output_stream.getvalue(),
        file_name="fixed_high_quality.pdf",
        mime="application/pdf"
    )

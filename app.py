import streamlit as st
import fitz  # PyMuPDF
import io

st.title("PDF座標補正API")

# ファイルアップロード受け付け
uploaded_file = st.file_uploader("PDFを選択", type="pdf")

if uploaded_file:
    src_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    new_doc = fitz.open()
    
    # A3横サイズ
    target_width, target_height = 1191, 842
    
    for page in src_doc:
        # 高解像度で画像化（3倍）
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), colorspace=fitz.csRGB)
        new_page = new_doc.new_page(width=target_width, height=target_height)
        img_bytes = pix.tobytes("png")
        new_page.insert_image(new_page.rect, stream=img_bytes)
    
    # 変換後のPDFをメモリに保存
    output_stream = io.BytesIO()
    new_doc.save(output_stream)
    
    st.download_button(
        label="修正済みPDFをダウンロード",
        data=output_stream.getvalue(),
        file_name="fixed_standard.pdf",
        mime="application/pdf"
    )

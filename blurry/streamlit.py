# AUTOGENERATED! DO NOT EDIT! File to edit: 03_streamlit.ipynb (unless otherwise specified).

__all__ = ['uploaded_file', 'get_image_download_link']

# Cell
#from core import *
#from blurry.core import *
import blurry.core as bl
import streamlit as st
import numpy as np
import base64
from PIL import Image
from io import BytesIO

# Cell
st.title("Blurry Faces");
st.write("Upload any photo with people in it, and this tool will pixelate the faces.")
uploaded_file = st.file_uploader("Upload a photo:", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)

# Cell
def get_image_download_link(img):
    """Generates a link allowing the PIL image to be downloaded
    in:  PIL image
    out: href string

    Source: https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/19
    """
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download="blurredfaces.jpg">Download result</a>'
    return href

# Cell
if uploaded_file is not None:
    st.write("File uploaded, processing...")
    img = Image.open(uploaded_file)
    img_array = np.array(img)
    anon_img = bl.anonymize(img_array, mode='pixelate')
    anon_img_pil = Image.fromarray(anon_img)

    st.image(anon_img, caption=" ", use_column_width=True)
    st.markdown(get_image_download_link(anon_img_pil), unsafe_allow_html=True)
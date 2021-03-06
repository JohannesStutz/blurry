# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['show_cv2', 'blur', 'pixelate', 'find_faces', 'blur_areas', 'anonymize', 'load_img', 'path',
           'get_image_download_link', 'img1', 'img2', 'img3', 'example', 'img_file', 'uploaded_file']

# Cell
import cv2
import numpy as np
import fastcore
import math
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

### For Streamlit ###
import streamlit as st
import base64
from io import BytesIO

# Cell
def show_cv2(img: np.ndarray) -> None:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    display(Image.fromarray(img))

# Cell
def blur(img: np.ndarray, factor=1, sigma_x=0) -> np.ndarray:
    h, w, _ = img.shape
    kernel_size = max(w,h) / 3
    kernel_size *= factor
    kernel_size = math.ceil(kernel_size)
    # Make sure that kernel size is an odd number
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma_x)

# Cell
def pixelate(img: np.ndarray, factor=1) -> np.ndarray:
    h, w, _ = img.shape
    aspect_ratio = h/w
    # New sizes
    small_h, small_w = 10/factor*aspect_ratio, 10/factor
    # Make sure resized version is at least 1 pixel in both dimensions and Integer
    small_h, small_w = int(max(1, small_h)), int(max(1, small_w))
    small = cv2.resize(img, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
    output = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    return output

# Cell
def find_faces(img):
    "Finds faces in a picture and returns tuples of (x, y, w, h) for each face"
    assert Path('haarcascade_frontalface_default.xml').is_file(), "haarcascade file not found"
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

# Cell
def blur_areas(img, areas, factor=1, blur_func=blur):
    """
    Blurs defined areas in a cv2 image.

    Inputs:
    img: cv2 image in BGR format
    areas: tuples of (x, y, w, h)
    factor: increase (>1.0) or decrease (<1.0) default blurring
    degrade_func: `blur` or `pixelate` (or any function that takes
        the arguments `image` and `factor`)

    Returns:
    cv2 image in BGR format
    """

    for (x, y, w, h) in areas:
        y = int(y - 0.1*h)
        h = int(1.25*h)
        img[y:y+h,x:x+w] = blur_func(img[y:y+h,x:x+w], factor=factor)

    return img

# Cell
def anonymize(img, factor=1, mode='blur', convert2rgb=False)->np.ndarray:
    faces = find_faces(img)
    if mode == 'pixelate':
        blur_func = pixelate
    else:
        blur_func = blur
    img = blur_areas(img, faces, factor=factor, blur_func=blur_func)
    if convert2rgb:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

# Cell
def load_img(fn):
    img = cv2.imread(str(fn))
    assert isinstance(img, np.ndarray), "Image file not found"
    return img

# Cell
path = Path('test_images')

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
st.title("Blurry Faces");
st.write("Upload any photo with people in it, and this tool will pixelate the faces.")

# Cell
img1 = path/'group.jpg'
img2 = path/'group_closer.jpg'
img3 = path/'crowd.jpg'
st.image([Image.open(img1), Image.open(img2), Image.open(img3)], width=200)
example = st.radio("Choose an example image", ["Group", "Small group", "Large crowd"])
img_file = None
if example == "Group":
    img_file = img1
elif example == "Small group":
    img_file = img2
elif example == "Large crowd":
    img_file = img3

# Cell
uploaded_file = st.file_uploader("Or upload a photo:", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)

# Cell
if uploaded_file or img_file:
    if uploaded_file: file = uploaded_file
    elif img_file: file = img_file
    #st.write("Processing...")
    img = Image.open(file)
    img_array = np.array(img)
    anon_img = anonymize(img_array, mode='pixelate')
    anon_img_pil = Image.fromarray(anon_img)

    st.image(anon_img, caption=" ", use_column_width='auto')
    st.markdown(get_image_download_link(anon_img_pil), unsafe_allow_html=True)
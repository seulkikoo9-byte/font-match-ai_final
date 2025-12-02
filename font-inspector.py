import streamlit as st
from PIL import Image
import imagehash
import numpy as np
import os

FONTS_FOLDER = "fonts"

def load_font_samples():
    font_samples = {}
    for file in os.listdir(FONTS_FOLDER):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            img = Image.open(os.path.join(FONTS_FOLDER, file))
            font_samples[file] = img
    return font_samples

def hash_image(img):
    return imagehash.average_hash(img)

def find_best_match(uploaded_img, font_samples):
    uploaded_hash = hash_image(uploaded_img)

    best_score = 999
    best_font = None
    for name, font_img in font_samples.items():
        score = abs(uploaded_hash - hash_image(font_img))
        if score < best_score:
            best_score = score
            best_font = name
    return best_font, best_score

st.title("AI 글꼴(Font) 자동 인식기")
st.write("이미지를 업로드하면 가장 유사한 글꼴을 찾아줍니다.")

font_samples = load_font_samples()

uploaded_file = st.file_uploader("텍스트 이미지 업로드", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드한 이미지", use_column_width=True)

    best_font, score = find_best_match(img, font_samples)

    st.subheader("추천 글꼴 결과")
    st.write(f"**가장 유사한 글꼴:** {best_font}")
    st.write(f"**유사도 점수:** {score}")

    st.write("아래는 비교된 예시 글꼴 이미지입니다.")
    st.image(font_samples[best_font])

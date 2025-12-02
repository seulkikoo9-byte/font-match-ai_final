import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import imagehash
import numpy as np


# -------------------------------
# 1) 코드 내부에서 글꼴 샘플 생성
# -------------------------------

def generate_font_image(text, font_path, size=80, image_size=(400, 150)):
    """지정한 폰트로 텍스트 이미지를 생성"""
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size)

    # 텍스트 중앙 정렬
    w, h = draw.textsize(text, font=font)
    pos = ((image_size[0] - w) / 2, (image_size[1] - h) / 2)
    draw.text(pos, text, fill="black", font=font)
    return img


# 비교용 폰트들 (시스템 기본 폰트 사용)
AVAILABLE_FONTS = {
    "DejaVuSans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "DejaVuSerif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "DejaVuSansMono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
}

# 미리 렌더링된 “기준 이미지” 생성
def load_internal_fonts():
    samples = {}
    for name, path in AVAILABLE_FONTS.items():
        try:
            img = generate_font_image("Sample Text", path)
            samples[name] = img
        except:
            pass
    return samples


# -------------------------------
# 2) 이미지 해시 비교
# -------------------------------

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


# -------------------------------
# 3) Streamlit UI
# -------------------------------

st.title("AI 글꼴(Font) 자동 인식기 — fonts 폴더 없이 작동")

st.write("이미지를 업로드하면 내부 기본 폰트와 비교하여 가장 유사한 글꼴을 추천합니다.")

font_samples = load_internal_fonts()

uploaded_file = st.file_uploader("텍스트 이미지 업로드", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="업로드한 이미지", use_column_width=True)

    best_font, score = find_best_match(img, font_samples)

    st.subheader("추천 글꼴 결과")
    st.write(f"**가장 유사한 글꼴:** {best_font}")
    st.write(f"**유사도 점수:** {score}")

    st.write("비교에 사용된 샘플 폰트 미리보기:")
    st.image(font_samples[best_font])

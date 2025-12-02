{\rtf1\ansi\ansicpg949\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
from PIL import Image\
import imagehash\
import numpy as np\
import os\
\
# \uc0\u49368 \u54540  \u44544 \u44852  \u51060 \u48120 \u51648  \u54260 \u45908  (fonts/\u50504 \u50640  .png \u54028 \u51068  \u50668 \u47084  \u44060 )\
FONTS_FOLDER = "fonts"\
\
def load_font_samples():\
    font_samples = \{\}\
    for file in os.listdir(FONTS_FOLDER):\
        if file.lower().endswith((".png", ".jpg", ".jpeg")):\
            img = Image.open(os.path.join(FONTS_FOLDER, file))\
            font_samples[file] = img\
    return font_samples\
\
def hash_image(img):\
    return imagehash.average_hash(img)\
\
def find_best_match(uploaded_img, font_samples):\
    uploaded_hash = hash_image(uploaded_img)\
\
    best_score = 999\
    best_font = None\
    for name, font_img in font_samples.items():\
        score = abs(uploaded_hash - hash_image(font_img))\
        if score < best_score:\
            best_score = score\
            best_font = name\
    return best_font, best_score\
\
st.title("AI \uc0\u44544 \u44852 (Font) \u51088 \u46041  \u51064 \u49885 \u44592 ")\
st.write("\uc0\u51060 \u48120 \u51648 \u47484  \u50629 \u47196 \u46300 \u54616 \u47732  \u44032 \u51109  \u50976 \u49324 \u54620  \u44544 \u44852 \u51012  \u52286 \u50500 \u51469 \u45768 \u45796 .")\
\
font_samples = load_font_samples()\
\
uploaded_file = st.file_uploader("\uc0\u53581 \u49828 \u53944  \u51060 \u48120 \u51648  \u50629 \u47196 \u46300 ", type=["png", "jpg", "jpeg"])\
\
if uploaded_file:\
    img = Image.open(uploaded_file)\
    st.image(img, caption="\uc0\u50629 \u47196 \u46300 \u54620  \u51060 \u48120 \u51648 ", use_column_width=True)\
\
    best_font, score = find_best_match(img, font_samples)\
\
    st.subheader("\uc0\u52628 \u52380  \u44544 \u44852  \u44208 \u44284 ")\
    st.write(f"**\uc0\u44032 \u51109  \u50976 \u49324 \u54620  \u44544 \u44852 :** \{best_font\}")\
    st.write(f"**\uc0\u50976 \u49324 \u46020  \u51216 \u49688 :** \{score\}")\
\
    st.write("\uc0\u50500 \u47000 \u45716  \u48708 \u44368 \u46108  \u50696 \u49884  \u44544 \u44852  \u51060 \u48120 \u51648 \u51077 \u45768 \u45796 .")\
    st.image(font_samples[best_font])\
}
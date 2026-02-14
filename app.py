# DeepTrace-Lite
# © 2026 Muneeza-Khan
# All Rights Reserved

import streamlit as st
import pandas as pd
from frame_analysis import analyze_video_frames
from audio_analysis import analyze_audio
from metadata_analysis import analyze_metadata
from risk_engine import calculate_risk

st.set_page_config(page_title="DeepTrace-Lite", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>
body {background-color:#fff0f5; font-family:'Times New Roman', serif;}
h1,h2,h3 {font-family:'Algerian','Backesrsvile Old Face', serif; color:#b03060; text-align:center;}
.short-desc {text-align:center; font-size:18px; color:#8b008b; margin-bottom:20px;}
div[data-testid="stFileUploader"] {background-color:#ffe4ec; padding:25px; border-radius:15px; margin-bottom:10px;}
.stFileUploader label {color:black; font-weight:bold;}
.stButton>button {background-color:#ff69b4; color:white; border-radius:12px; padding:10px 25px; font-size:16px;}
.popup {border-radius:12px; padding:15px; text-align:center; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1>🕵️‍♀️ DeepTrace-Lite</h1>", unsafe_allow_html=True)
st.markdown("<h3>Media Authenticity Risk Analyzer</h3>", unsafe_allow_html=True)
st.markdown('<p class="short-desc">A lightweight AI-powered media authenticity analyzer designed to detect potential deepfake or manipulated content in videos and audio. The tool evaluates video frames, audio patterns, and metadata to generate a comprehensive risk score, helping users identify suspicious or AI-generated media while providing a clear, risk-based breakdown of detected anomalies.</p>', unsafe_allow_html=True)
st.markdown("---")

# ---------- FILE UPLOADER ----------
uploaded_file = st.file_uploader("Upload video/audio 💗", type=["mp4","mov","avi","mp3","wav"])

if uploaded_file:
    filename = uploaded_file.name
    with open("temp_media","wb") as f: f.write(uploaded_file.read())
    is_audio = filename.lower().endswith(('.mp3','.wav'))

    with st.spinner("Analyzing media... 💕"):
        frame_risk = analyze_video_frames("temp_media") if not is_audio else 0
        audio_risk, audio_label = analyze_audio("temp_media")
        metadata_risk = analyze_metadata("temp_media")
        final_risk = calculate_risk(frame_risk, audio_risk, metadata_risk)

    # ---------- FILE NAME COLOR ----------
    color = "red" if final_risk>50 else "yellow" if final_risk==50 else "green"
    st.markdown(f'<p style="color:{color}; font-weight:bold; font-size:18px;">Uploaded File: {filename}</p>', unsafe_allow_html=True)

    # ---------- FINAL RISK POPUP ----------
    if final_risk>50:
        popup_color = "#FF6B6B"
        popup_msg = "💔 High Risk: Manual verification recommended!"
    elif final_risk==50:
        popup_color = "#FFD93D"
        popup_msg = "⚠️ Medium Risk: Review suggested."
    else:
        popup_color = "#6BCB77"
        popup_msg = "💖 Low Risk: Media appears authentic!"

    st.markdown(f'<div class="popup" style="background-color:{popup_color};">{popup_msg}<br>Deepfake Risk Score: {final_risk}/100</div>', unsafe_allow_html=True)

    # ---------- RISK BREAKDOWN BARS ----------
    st.markdown("### 🎀 Risk Breakdown")
    df = pd.DataFrame({
        'Risk Type': ['Frame Analysis','Audio Analysis','Metadata'],
        'Score': [frame_risk,audio_risk,metadata_risk],
    })

    for idx,row in df.iterrows():
        # Determine bar color based on score
        if row['Score']>50: bar_color="#FF6B6B"
        elif row['Score']==50: bar_color="#FFD93D"
        else: bar_color="#6BCB77"

        # Add AI/Human label for Audio
        label = f"{row['Score']} ({audio_label})" if row['Risk Type']=="Audio Analysis" else str(row['Score'])

        st.markdown(f"<p style='font-weight:bold'>{row['Risk Type']}: {label}</p>", unsafe_allow_html=True)
        st.progress(row['Score']/100)


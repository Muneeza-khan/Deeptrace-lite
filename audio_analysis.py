from pymediainfo import MediaInfo
import numpy as np
import librosa

def analyze_audio(media_path):
    """
    Analyze audio for unnatural bitrate + AI-generated voice detection.
    Returns: risk_score (0-30), ai_label
    """
    risk = 0
    ai_label = "Human voice"

    # ---------- Bitrate check ----------
    media_info = MediaInfo.parse(media_path)
    for track in media_info.tracks:
        if track.track_type == "Audio" and track.bit_rate:
            risk += 10 if int(track.bit_rate) > 320000 else 5

    # ---------- AI voice detection ----------
    try:
        y, sr = librosa.load(media_path, sr=None)
        pitches, mags = librosa.piptrack(y=y, sr=sr)
        pitches = pitches[mags > np.median(mags)]
        pitch_std = np.std(pitches) if len(pitches) > 1 else 0
        if pitch_std < 20:  # monotone → likely AI
            risk += 10
            ai_label = "Likely AI-generated voice"
    except:
        risk += 5

    return min(risk,30), ai_label

def calculate_risk(frame_risk, audio_risk, metadata_risk):
    """Combine all risks into final score (0-100)"""
    return min(frame_risk + audio_risk + metadata_risk, 100)

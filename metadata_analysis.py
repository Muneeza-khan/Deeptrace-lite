from pymediainfo import MediaInfo

def analyze_metadata(media_path):
    """
    Basic metadata analysis for file inconsistencies.
    Returns risk score (0-30)
    """
    try:
        media_info = MediaInfo.parse(media_path)
        for track in media_info.tracks:
            if track.track_type == "General" and track.duration:
                dur = float(track.duration)
                if dur < 1000: return 10
    except:
        return 5
    return 5

import cv2
import numpy as np

def analyze_video_frames(video_path):
    """
    Analyze video frames for blur artifacts.
    Returns risk score based on average blur.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened(): return 0

    blur_values = []
    frames_checked = 0
    while frames_checked < 30:
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_values.append(blur_score)
        frames_checked += 1

    cap.release()
    if not blur_values: return 0
    avg_blur = np.mean(blur_values)

    # Risk scoring
    if avg_blur < 150: return 50
    elif avg_blur < 300: return 20
    else: return 0

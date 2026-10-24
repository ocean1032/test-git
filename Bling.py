import cv2
import numpy as np
import mediapipe as mp
import time
import math

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Fullscreen
cv2.namedWindow("Magic Fingers", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Magic Fingers", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Ngón tay tip và MCP (gốc ngón)
FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_BASE = [2, 5, 9, 13, 17]

# Cooldown mỗi ngón (theo từng ngón của mỗi tay)
cooldowns = {}  # key: (hand_index, finger_index) -> time
COOLDOWN_TIME = 0  # giây

angle_offset = 0  # góc xoay cho hiệu ứng

def draw_rotating_bling(img, x, y, angle=0, color=(0, 255, 255)):
    cv2.circle(img, (x, y), 20, color, 2)
    cv2.circle(img, (x, y), 8, color, -1)
    for a in range(0, 360, 45):
        rad = math.radians(a + angle)
        dx = int(30 * math.cos(rad))
        dy = int(30 * math.sin(rad))
        cv2.line(img, (x, y), (x + dx, y + dy), color, 1)

def finger_extended(lm_tip, lm_base, threshold=0.2):
    dx = lm_tip.x - lm_base.x
    dy = lm_tip.y - lm_base.y
    distance = math.sqrt(dx**2 + dy**2)
    return distance > threshold

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            for i, tip_id in enumerate(FINGER_TIPS):
                base_id = FINGER_BASE[i]
                tip = hand_landmarks.landmark[tip_id]
                base = hand_landmarks.landmark[base_id]

                if finger_extended(tip, base):
                    key = (hand_idx, tip_id)
                    last_time = cooldowns.get(key, 0)

                    if current_time - last_time >= COOLDOWN_TIME:
                        cx, cy = int(tip.x * w), int(tip.y * h)
                        draw_rotating_bling(img, cx, cy, angle_offset)
                        cooldowns[key] = current_time  # đặt lại cooldown

    angle_offset = (angle_offset + 5) % 360  # quay dần

    cv2.imshow("Magic Fingers", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
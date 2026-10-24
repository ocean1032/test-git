import cv2
import numpy as np
import mediapipe as mp

# Load ảnh vòng phép có nền trong suốt
circle = cv2.imread(r"magic_circle.png", cv2.IMREAD_UNCHANGED)

# Nếu ảnh không có kênh alpha, thêm vào
if circle.shape[2] == 3:
    circle = cv2.cvtColor(circle, cv2.COLOR_BGR2BGRA)

# Thiết lập nhận diện tay
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Mở webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Toàn màn hình
cv2.namedWindow("Dr. Strange Effect", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Dr. Strange Effect", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

angle = 0
scale = 3.0  # 👈 scale mặc định ban đầu

def overlay_transparent(background, overlay, x, y, angle=0, scale=1.0):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    if angle != 0:
        (h, w) = overlay.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        overlay = cv2.warpAffine(overlay, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    h, w = overlay.shape[:2]
    h_bg, w_bg = background.shape[:2]

    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x + w, w_bg), min(y + h, h_bg)

    if x1 >= x2 or y1 >= y2:
        return background

    overlay_crop = overlay[(y1 - y):(y2 - y), (x1 - x):(x2 - x)]
    b, g, r, a = cv2.split(overlay_crop)
    mask = a / 255.0

    for c in range(3):
        background[y1:y2, x1:x2, c] = background[y1:y2, x1:x2, c] * (1 - mask) + overlay_crop[:, :, c] * mask

    return background

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            cx = int(hand_landmarks.landmark[9].x * img.shape[1])
            cy = int(hand_landmarks.landmark[9].y * img.shape[0])

            size = int(100 * scale)  # căn giữa theo kích thước
            img = overlay_transparent(img, circle.copy(), cx - size, cy - size, angle, scale=scale)

    angle = (angle + 2) % 360

    # Hiển thị thông tin scale
    cv2.putText(img, f"Scale: {scale:.1f}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

    cv2.imshow("Dr. Strange Effect", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('+') or key == ord('='):  # một số bàn phím dùng '=' thay vì '+'
        scale = min(scale + 0.1, 10.0)
    elif key == ord('-') or key == ord('_'):
        scale = max(scale - 0.1, 0.3)

cap.release()
cv2.destroyAllWindows()
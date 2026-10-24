import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Khởi tạo Hands với chế độ theo dõi
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # hoặc 1920
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # hoặc 1080

pTime = 0  # thời gian khung hình trước

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # ← Lật ảnh theo chiều ngang để không bị ngược

    # Chuyển ảnh thành RGB vì mediapipe yêu cầu
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Nếu phát hiện được tay
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Vẽ các điểm và khớp nối bàn tay
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Tính FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime + 1e-5)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Hiển thị
    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
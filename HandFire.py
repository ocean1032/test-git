import cv2
import mediapipe as mp
import pygame
import numpy as np
import math
import time

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Initialize OpenCV
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
clock = pygame.time.Clock()

# Particle class for fire effect
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = np.random.randint(4, 8)
        self.color = color
        self.alpha = 255
        self.vel = [np.random.uniform(-1, 1), np.random.uniform(-3, -1)]

    def update(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        self.alpha -= 5

    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (self.radius, self.radius), self.radius)
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

# Particle system
particles = []

# Finger tip landmarks
FINGER_TIPS = [4, 8, 12, 16, 20]

# Utility to detect if hand is open or closed
def is_hand_open(landmarks):
    fingers_open = 0
    for tip_id in FINGER_TIPS[1:]:  # Skip thumb
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            fingers_open += 1
    return fingers_open >= 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Thoát khi nhấn ESC
                running = False

    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Convert frame to Pygame surface and display as background
    frame_surface = pygame.surfarray.make_surface(np.flipud(np.rot90(rgb)))
    frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))
    screen.blit(frame_surface, (0, 0))

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = frame.shape
        landmark_list = hand_landmarks.landmark
        cx = int(landmark_list[9].x * w)
        cy = int(landmark_list[9].y * h)

        open_hand = is_hand_open(landmark_list)

        if open_hand:
            for tip_id in FINGER_TIPS:
                lx = int(landmark_list[tip_id].x * w)
                ly = int(landmark_list[tip_id].y * h)
                for _ in range(3):
                    particles.append(Particle(lx, ly, (255, 140, 0)))
        else:
            for _ in range(10):
                particles.append(Particle(cx, cy, (255, 80, 10)))

    for p in particles[:]:
        p.update()
        p.draw(screen)
        if p.alpha <= 0:
            particles.remove(p)

    pygame.display.flip()
    clock.tick(30)

cap.release()
pygame.quit()
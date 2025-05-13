import cv2
import numpy as np
import random

# Window size
width, height = 640, 480

# Ball properties
ball_radius = 20
ball_x = random.randint(ball_radius, width - ball_radius)
ball_y = 0
ball_speed = 5

# Paddle properties
paddle_width = 100
paddle_height = 20
paddle_y = height - 50

# Score
score = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (width, height))

    # Detect hand color (you can use a red marker/glove for simplicity)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    paddle_x = width // 2  # default center

    if contours:
        cnt = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(cnt)
        paddle_x = x + w // 2 - paddle_width // 2

    # Draw paddle
    cv2.rectangle(frame, (paddle_x, paddle_y), (paddle_x + paddle_width, paddle_y + paddle_height), (255, 0, 0), -1)

    # Move ball
    ball_y += ball_speed
    if ball_y > height:
        ball_y = 0
        ball_x = random.randint(ball_radius, width - ball_radius)

    # Check for collision
    if (paddle_y < ball_y + ball_radius < paddle_y + paddle_height) and (paddle_x < ball_x < paddle_x + paddle_width):
        score += 1
        ball_y = 0
        ball_x = random.randint(ball_radius, width - ball_radius)

    # Draw ball
    cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 255, 0), -1)

    # Display score
    cv2.putText(frame, f'Score: {score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Catch the Ball Game', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

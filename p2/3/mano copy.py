import math
import cv2
import mediapipe as mp
from pynput.mouse import Button, Controller
import pyautogui

MOUSE = Controller()

cap = cv2.VideoCapture(0)

cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

screen_width, screen_height = pyautogui.size()

MPH = mp.solutions.hands
MPD = mp.solutions.drawing_utils
hands = MPH.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

pinch = False

def calcularDistanciaEntreDedos(image, hand_lamdmarks, handNo = 0):
    global pinch
    
    if hand_lamdmarks is not None:
        landmarks = hand_lamdmarks[handNo].landmark

        finger_tip_x = int((landmarks[8].x))
        finger_tip_y = int((landmarks[8].y))

        cv2.line(image, (finger_tip_x, finger_tip_y), (000, 000, 255), 2)

def drawHandLandmarks(img, hand_landmarks):
    for landmark in hand_landmarks:
        MPD.draw_landmarks(img, landmark, MPH.HAND_CONNECTIONS)
    

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    print(image)
    results = hands.process(image)
    print(results.multi_hand_landmarks)
    H_landmarks = results.multi_hand_landmarks
    print(image, H_landmarks)
    drawHandLandmarks(image, H_landmarks)

    if not success:
        print("OH NO D:")
        break
    if cv2.waitKey(1) == 32:
        break
    cv2.imshow("",image)

cv2.destroyAllWindows()
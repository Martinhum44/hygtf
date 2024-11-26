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
hands = MPH.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.2)

tipIds = [4, 8, 12, 16, 20]

pinch = False

def calcularDistanciaEntreDedos(image, hand_lamdmarks, handNo = 0):
    global pinch
    
    if hand_lamdmarks is not None:
        landmarks = hand_lamdmarks[handNo].landmark

        finger_tip_x = int((landmarks[8].x)*cap_width)
        finger_tip_y = int((landmarks[8].y)*cap_height)

        thumb_tip_x = int((landmarks[4].x)*cap_width)
        thumb_tip_y = int((landmarks[4].y)*cap_height)

        cv2.line(image, (finger_tip_x, finger_tip_y), (thumb_tip_x, thumb_tip_y),(000, 000, 255), 2)
        try:
            relative_x = (screen_width/cap_width)*finger_tip_x
            relative_y = (screen_width/cap_width)*finger_tip_y
            MOUSE.position = (relative_x,relative_y)
            return math.sqrt((thumb_tip_y-finger_tip_y)**2 + (thumb_tip_x-finger_tip_x))
        except Exception:
            return 9999

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
    if H_landmarks is not None:
        drawHandLandmarks(image, H_landmarks)
        distancia = calcularDistanciaEntreDedos(image, H_landmarks)
        cv2.putText(image, f"Distancia: {distancia}", (40,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (000,000,000), 1)

        if distancia > 40:
            if pinch == True:
                print("Pinch = True")
                pinch = False
                MOUSE.release(Button.left)

        if distancia <= 40:
            if pinch == False:
                print("Pinch = False")
                pinch = True
                MOUSE.press(Button.left)

    if not success:
        print("OH NO D:")
        break
    if cv2.waitKey(1) == 32:
        break
    cv2.imshow("",image)

cv2.destroyAllWindows()
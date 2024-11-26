import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
MPH = mp.solutions.hands
MPD = mp.solutions.drawing_utils
hands = MPH.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

def drawHandLandmarks(img, hand_landmarks):
    for landmark in hand_landmarks:
        MPD.draw_landmarks(img, landmark, MPH.HAND_CONNECTIONS)

def countFingers(img, hand_landmarks, HANDNO=0):
    tipIds = (4, 8, 12, 16, 20)
    landmarks = hand_landmarks[HANDNO].landmark
    total = 0
    for fingerTip in tipIds:
        finger_tip_y = landmarks[fingerTip].y
        finger_bottom_y = landmarks[fingerTip-2].y
        if tipIds != 4:
            if finger_tip_y < finger_bottom_y:
                total += 1
                print("El dedo con id ",fingerTip," esta abierto!!!!!!!")
            if finger_tip_y > finger_bottom_y:
                print("El dedo con id ",fingerTip," esta cerrado!!!!!!!")
    return total
    

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    results = hands.process(image)
    H_landmarks = results.multi_hand_landmarks
    print(image, H_landmarks)
    if H_landmarks is not None:
        drawHandLandmarks(image, H_landmarks)
        openFingers = countFingers(image,H_landmarks)
        cv2.putText(image, f"Hay {openFingers} dedos abiertos",(50,50),cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (000,000,000), 2)
    if not success:
        print("OH NO D:")
        break
    if cv2.waitKey(1) == 32:
        break
    cv2.imshow("",image)

cv2.destroyAllWindows()
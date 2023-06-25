import cv2
import time
from pose import PoseDetector
from pynput.keyboard import Key, Controller
from Util import PutMark, PutLine, PutText
import pyautogui

cap = cv2.VideoCapture(0)
detector = PoseDetector()
WIDTH, HEIGHT = 1280, 960
keyboard = Controller()

draw = True
previousTime = 0

LEFT_MARGIN = int(WIDTH/2) + 150
RIGHT_MARGIN = int(WIDTH/2) - 150
DOWN_MARGIN = HEIGHT - 150

while True: 

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, [WIDTH, HEIGHT])
    img = detector.findPose(img)
    lmList = detector.findPosition(img,False)

    if len(lmList) != 0:
        marks = {
            "left_foot": [lmList[31][1],lmList[31][2]],
            "right_foot": [lmList[32][1],lmList[32][2]],
            "nose": [lmList[0][1],lmList[0][2]]
        }

        if draw:
            PutMark(img, lmList[0][1], lmList[0][2],(255,0,255))
            PutText(img, f"X={lmList[0][1]}",WIDTH - 300, 75, (255,0,255))

            PutMark(img, lmList[31][1], lmList[31][2],(0,255,255))
            PutText(img, f"Y={HEIGHT - lmList[31][2]}",WIDTH - 300, HEIGHT - 50,(0,255,255))

            PutMark(img, lmList[32][1], lmList[32][2],(0,0,255))
            PutText(img, f"Y={HEIGHT - lmList[32][2]}",70, HEIGHT - 50, (0,0,255))

            PutMark(img, lmList[20][1], lmList[20][2],(255,255,0))
            PutText(img, f"X={lmList[20][1]}, Y={HEIGHT - lmList[20][2]}",int((WIDTH / 2) - 300), 75, (255,255,0))

            #divide a tela em 3 áreas, LEFT, RIGH e JUMP
            PutLine(img, (LEFT_MARGIN,0),(LEFT_MARGIN,HEIGHT))
            PutLine(img, (RIGHT_MARGIN,0),(RIGHT_MARGIN,HEIGHT))
            PutLine(img, (0, DOWN_MARGIN),(WIDTH, DOWN_MARGIN))

            PutText(img, "LEFT",int((WIDTH / 2) - 500), int((HEIGHT / 2) - 300))
            PutText(img, "RIGHT",int((WIDTH / 2) + 300), int((HEIGHT / 2) - 300))
            PutText(img, "JUMP",int((WIDTH / 2) - 100), (HEIGHT - 200))

        angle = detector.findAngle(img, 13, 11, 23, draw)

        #detecta a colisão das landmarks nas áreas e aperta as respectivas teclas
        if (HEIGHT - marks["left_foot"][1]) > 150 and (HEIGHT - marks["right_foot"][1]) > 150:
            keyboard.press(Key.space)
            PutText(img, "JUMP",int((WIDTH / 2) - 100), HEIGHT - 200, (0,255,0))

        if lmList[0][1] > (int(WIDTH/2) + 150):
            keyboard.press("d")
            PutText(img, "RIGHT",int((WIDTH / 2) + 300), int((HEIGHT / 2) - 300), (0,255,0))
        
        if lmList[0][1] < (int(WIDTH/2) - 150):
            keyboard.press("a")
            PutText(img, "LEFT",int((WIDTH / 2) - 500), int((HEIGHT / 2) - 300), (0,255,0))
            
        keyboard.release("a")
        keyboard.release(Key.space)
        keyboard.release("d")
            
    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime

    PutText(img, str(int(fps)),70, 75, (255, 0, 0))
    cv2.imshow("image", img)

    cv2.waitKey(1)
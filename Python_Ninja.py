import cv2
import pose
import random
import time
import Util

cap = cv2.VideoCapture(0)
pTime = 0
detector = pose.PoseDetector()

acceleration = 1
pos_y = 1
pos_x = random.randint(10, 550)
size = random.randint(50, 100)
points = 0
miss = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findPose(img)
    lmList = detector.findPosition(img,False)
    if len(lmList) != 0:
        cv2.circle(img, (pos_x, pos_y), size, (0, 255, 255), cv2.FILLED)

        pos_y += acceleration
        acceleration += 1

        cv2.putText(img, (str(int(points))),(500, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
        cv2.putText(img, (str(int(miss))),(500, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
        Util.PutMark(img, lmList[19][1], lmList[19][2], (0,255,0))
        Util.PutMark(img, lmList[20][1], lmList[20][2], (255,0,0))

        if lmList[19][1] > pos_x - size and lmList[19][1] < pos_x + size and lmList[19][2] > pos_y - size and lmList[19][2] < pos_y + size or lmList[20][1] > pos_x - size and lmList[20][1] < pos_x + size and lmList[20][2] > pos_y - size and lmList[20][2] < pos_y + size:
                pos_y = 0
                pos_x = random.randint(10, 550)
                size = random.randint(25, 100)
                acceleration = 1
                points += 1
        elif pos_y > 600:
            pos_y = 1
            pos_x = random.randint(10, 550)
            size = random.randint(25, 100)
            acceleration = 1
            miss += 1

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
  

    cv2.putText(img, f'FPS={str(int(fps))}',(30, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    img = cv2.resize(img, [1280, 960])
    cv2.imshow("image", img) 
    if cv2.waitKey(1) & 0xFF == ord('q') or miss == 10 :
        break
cv2.destroyAllWindows()

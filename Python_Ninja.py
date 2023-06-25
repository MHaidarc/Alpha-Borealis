import cv2
import pose
import random
import time
import Util

cap = cv2.VideoCapture(0)
pTime = 0
detector = pose.PoseDetector()

ACC = 1
POS = 1
POSY = random.randint(10, 550)
TAM = 50
points = 0
miss = 0

#dificuldade = input("DIFICULDADE:")
#print("dificuldade selecionada:", dificuldade)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findPose(img)
    lmList = detector.findPosition(img,False)
    if len(lmList) != 0:
        cv2.circle(img, (POSY, POS), TAM, (0, 255, 255), cv2.FILLED)

        #if dificuldade == 'fácil':
        POS += ACC
        ACC += 1
        #elif dificuldade == 'médio':
        #    POS += ACC
        #    ACC += 2
        #elif dificuldade == 'difícil':
        #    POS += ACC
        #    ACC += 3

        cv2.putText(img, (str(int(points))),(500, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
        cv2.putText(img, (str(int(miss))),(500, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
        Util.PutMark(img, lmList[19][1], lmList[19][2], (0,255,0))
        Util.PutMark(img, lmList[20][1], lmList[20][2], (255,0,0))

        #eu não tenho a menor ideia de que porra é esse if, mas FUNCIONA, e eu estou cansada demais pra arrumar isso
        if lmList[19][1] > POSY - TAM and lmList[19][1] < POSY + TAM and lmList[19][2] > POS - TAM and lmList[19][2] < POS + TAM or lmList[20][1] > POSY - TAM and lmList[20][1] < POSY + TAM and lmList[20][2] > POS - TAM and lmList[20][2] < POS + TAM:
                POS = 0
                POSY = random.randint(10, 550)
                ACC = 1
                points += 1
        elif POS > 600:
            POS = 1
            POSY = random.randint(10, 550)
            ACC = 1
            miss += 1

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
  

    cv2.putText(img, str(int(fps)),(70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    img = cv2.resize(img, [1280, 960])
    cv2.imshow("image", img) 
    cv2.waitKey(1)
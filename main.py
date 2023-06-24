import cv2
import time
from pose import PoseDetector
from pynput.keyboard import Key, Controller

cap = cv2.VideoCapture(0)               # seta a webcam integrada como captura de vídeo
startTime = 0                           # previous time ---> para calcular o FPS
detector = PoseDetector()    # importa o detector de pose do módulo de detecção 

HEIGHT = 960
WIDTH = 1280
keyboard = Controller()

#loop infinito
while True: 

    success, img = cap.read() #lê a imagem da webcam integrada todos os frames
    img = cv2.flip(img, 1) #inverte a imagem no eixo y
    img = cv2.resize(img, [WIDTH, HEIGHT]) #aumenta o tamanho da imagem para 1280:960
    img = detector.findPose(img) #encontra a pose do jogador na imagem e não desenha os pontos e ligações
    lmList = detector.findPosition(img,False) #grava os pontos de landmark em uma lista mas não os desenha

    if len(lmList) != 0: #se o tamanho da lista de landmarks for diferente de 0

        #desenha círculos no nariz
        cv2.circle(img, (lmList[0][1], lmList[0][2]), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (lmList[0][1], lmList[0][2]), 20, (255,0,255), 2)
        cv2.putText(img, f"X={lmList[0][1]}",(WIDTH - 300, 75), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,255), 5)

        #desenha círculos no pé direito
        cv2.circle(img, (lmList[31][1], lmList[31][2]), 15, (0,255,255), cv2.FILLED)
        cv2.circle(img, (lmList[31][1], lmList[31][2]), 20, (0,255,255), 2)
        cv2.putText(img, f"Y={HEIGHT - lmList[31][2]}",(WIDTH - 300, HEIGHT - 50), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,255), 5)

        #desenha círculos no pé direito
        cv2.circle(img, (lmList[32][1], lmList[32][2]), 15, (0,0,255), cv2.FILLED)
        cv2.circle(img, (lmList[32][1], lmList[32][2]), 20, (0,0,255), 2)
        cv2.putText(img, f"Y={HEIGHT - lmList[32][2]}",(70, HEIGHT - 50), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 5)

        cv2.circle(img, (lmList[20][1], lmList[20][2]), 15, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, (lmList[20][1], lmList[20][2]), 20, (255, 255, 0), 2)
        cv2.putText(img, f"X={lmList[20][1]}, Y={HEIGHT - lmList[20][2]}",(int((WIDTH / 2) - 300), 75), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,0), 5)

        cv2.line(img, ((int(WIDTH/2)-150),0),((int(WIDTH/2)-150),HEIGHT),(0,0,255),4)
        cv2.line(img, ((int(WIDTH/2)+150),0),((int(WIDTH/2)+150),HEIGHT),(0,0,255),4)
        cv2.line(img, (0, (HEIGHT - 150)),(WIDTH, (HEIGHT - 150)),(0,0,255),4)

        cv2.putText(img, "LEFT",(int((WIDTH / 2) - 500), (int((HEIGHT / 2) - 300))), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 5)
        cv2.putText(img, "RIGHT",(int((WIDTH / 2) + 300), (int((HEIGHT / 2) - 300))), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 5)
        cv2.putText(img, "JUMP",(int((WIDTH / 2) - 100), (HEIGHT - 200)), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 5)

        #encontra o ângulo formado no braço direito
        #detector.findAngle(img, 14, 12, 24)
        #encontra o ângulo formado no braço esquerdo
        detector.findAngle(img, 13, 11, 23)

        if (HEIGHT - lmList[31][2]) > 150 and (HEIGHT - lmList[32][2]) > 150:
            keyboard.press(Key.space)
            cv2.putText(img, "JUMP",(int((WIDTH / 2) - 100), (HEIGHT - 200)), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,0), 5)

        keyboard.release(Key.space)

        if lmList[0][1] > (int(WIDTH/2) + 150):
            keyboard.press("d")
            cv2.putText(img, "RIGHT",(int((WIDTH / 2) + 300), (int((HEIGHT / 2) - 300))), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,0), 5)
        keyboard.release("d")
        
        if lmList[0][1] < (int(WIDTH/2) - 150):
            keyboard.press("a")
            cv2.putText(img, "LEFT",(int((WIDTH / 2) - 500), (int((HEIGHT / 2) - 300))), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,0), 5)
        keyboard.release("a")
            

    currentTime = time.time() #current time ---> tempo atual gravado
    fps = 1/(currentTime-startTime) #calcula o FPS dividindo 1 pela subtração do tempo atual e do anterior
    startTime = currentTime #tempo anterior = tempo atual

    cv2.putText(img, str(int(fps)),(70, 75), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5) #escreve o FPS na tela
    cv2.imshow("image", img) #mostra a imagem

    cv2.waitKey(1) #espera 1 frame para repetir o loop
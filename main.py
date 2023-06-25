import cv2
import time
from pose import PoseDetector
from pynput.keyboard import Key, Controller
from Util import PutMark, PutCircle, PutLine, PutText

cap = cv2.VideoCapture(0)               # seta a webcam integrada como captura de vídeo
previousTime = 0                           # previous time ---> para calcular o FPS
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
        PutMark(img, lmList[0][1], lmList[0][2],(255,0,255))
        PutText(img, f"X={lmList[0][1]}",WIDTH - 300, 75, (255,0,255))

        #desenha círculos nos pés
        PutMark(img, lmList[31][1], lmList[31][2],(0,255,255))
        PutText(img, f"Y={HEIGHT - lmList[31][2]}",WIDTH - 300, HEIGHT - 50,(0,255,255))

        PutMark(img, lmList[32][1], lmList[32][2],(0,0,255))
        PutText(img, f"Y={HEIGHT - lmList[32][2]}",70, HEIGHT - 50, (0,0,255))

        #desenha círculos na mão esquerda
        PutMark(img, lmList[20][1], lmList[20][2],(255,255,0))
        PutText(img, f"X={lmList[20][1]}, Y={HEIGHT - lmList[20][2]}",int((WIDTH / 2) - 300), 75, (255,255,0))

        #divide a tela em 3 áreas, LEFT, RIGH e JUMP
        PutLine(img, (int(WIDTH/2)-150,0),(int(WIDTH/2)-150,HEIGHT),(0,0,255))
        PutLine(img, (int(WIDTH/2)+150,0),(int(WIDTH/2)+150,HEIGHT),(0,0,255))
        PutLine(img, (0, HEIGHT - 150),(WIDTH, HEIGHT - 150),(0,0,255))

        PutText(img, "LEFT",int((WIDTH / 2) - 500), int((HEIGHT / 2) - 300))
        PutText(img, "RIGHT",int((WIDTH / 2) + 300), int((HEIGHT / 2) - 300))
        PutText(img, "JUMP",int((WIDTH / 2) - 100), (HEIGHT - 200))

        #encontra o ângulo formado no braço direito
        #detector.findAngle(img, 14, 12, 24)
        #encontra o ângulo formado no braço esquerdo
        detector.findAngle(img, 13, 11, 23)

        #detecta a colisão das landmarks nas áreas e aperta as respectivas teclas
        if (HEIGHT - lmList[31][2]) > 150 and (HEIGHT - lmList[32][2]) > 150:
            keyboard.press(Key.space)
            PutText(img, "JUMP",int((WIDTH / 2) - 100), HEIGHT - 200, (0,255,0))

        keyboard.release(Key.space)

        if lmList[0][1] > (int(WIDTH/2) + 150):
            keyboard.press("d")
            PutText(img, "RIGHT",int((WIDTH / 2) + 300), int((HEIGHT / 2) - 300), (0,255,0))
        keyboard.release("d")
        
        if lmList[0][1] < (int(WIDTH/2) - 150):
            keyboard.press("a")
            PutText(img, "LEFT",int((WIDTH / 2) - 500), int((HEIGHT / 2) - 300), (0,255,0))
        keyboard.release("a")
            

    currentTime = time.time() #current time ---> tempo atual gravado
    fps = 1/(currentTime-previousTime) #calcula o FPS dividindo 1 pela subtração do tempo atual e do anterior
    previousTime = currentTime #tempo anterior = tempo atual

    PutText(img, str(int(fps)),70, 75, (255, 0, 0)) #escreve o FPS na tela
    cv2.imshow("image", img) #mostra a imagem

    cv2.waitKey(1) #espera 1 frame para repetir o loop
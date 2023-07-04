import cv2
from Pose import Capture, Util
from pynput.keyboard import Key, Controller

class Detector:
    def __init__(self, width=1280, height=960, left_margin=..., right_margin=..., down_margin=..., canDraw=True, title=...):
        self.width = width
        self.height = height
        self.left_margin = left_margin
        self.right_margin = right_margin
        self.down_margin = down_margin
        self.center = (int(width/2),int(height/2))
        self.title = title

        self.cap = cv2.VideoCapture(0)
        self.capture = Capture()
        self.keyboard = Controller()
        self.draw = Util.Draw(canDraw)

        self.__main_loop()

    def __press(self, key):
        self.keyboard.press(Key.space if key=="space" else key)
        self.keyboard.release(Key.space if key=="space" else key)

    def __process(self, marks):
        self.draw.PutLine((self.left_margin,0),(self.left_margin,self.height), self.draw.red)
        self.draw.PutLine((self.right_margin,0),(self.right_margin,self.height), self.draw.red)
        self.draw.PutLine((0, self.down_margin),(self.width, self.down_margin), self.draw.red)

        self.draw.PutText("LEFT",(self.left_margin - 200, 200), self.draw.red)
        self.draw.PutText("RIGHT",(self.right_margin + 10, 200), self.draw.red)
        self.draw.PutText("JUMP",(self.center[0] - 100, self.height - 200), self.draw.red)
        
        self.draw.PutMark(marks[0], self.draw.green)
        self.draw.PutMark(marks[31], self.draw.magenta)
        self.draw.PutMark(marks[32], self.draw.magenta)

        self.draw.PutMark(self.capture.hand["right"], self.draw.cian)
        self.draw.PutMark(self.capture.hand["left"], self.draw.cian)

        if self.height - marks[31][1] > self.down_margin and self.height - marks[32][1] > self.down_margin:
            self.__press("space")
            self.draw.PutText("JUMP",(self.center[0] - 100, self.height - 200), self.draw.green)

        if marks["nose"][0] > self.right_margin:
            self.__press("d")
            self.draw.PutText("RIGHT",(self.right_margin + 10, 200), self.draw.green)
        
        if marks["nose"][0] < self.left_margin:
            self.__press("a")
            self.draw.PutText("LEFT",(self.left_margin - 200, 200), self.draw.green)

    def __main_loop(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (WIDTH, HEIGHT))

            self.capture.Read(img)
            self.draw.UpdateImage(img)

            marks = self.capture.marks

            if success and marks != None:
                self.__process(marks)

                cv2.imshow(self.title, img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    WIDTH, HEIGHT = 1280, 600
    LEFT_MARGIN = int(WIDTH/2) - 150
    RIGHT_MARGIN = int(WIDTH/2) + 150
    DOWN_MARGIN = HEIGHT - 150

    detec = Detector(
        width=WIDTH,
        height=HEIGHT,
        left_margin=LEFT_MARGIN,
        right_margin=RIGHT_MARGIN,
        down_margin=DOWN_MARGIN,
        canDraw=True,
        title = "Alpha Borealis Detector"
    )
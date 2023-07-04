import cv2

class Draw:
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    yellow = (255,255,0)
    cian = (0,255,255)
    magenta = (255,255,0)

    def __init__(self, canDraw):
        self.canDraw = canDraw

    def UpdateImage(self, img):
        self.img = img

    def PutMark(self,pos,color=(0,0,255)):
        self.PutCircle((pos[0],pos[1]),15,-1, color)
        self.PutCircle((pos[0],pos[1]),20,2, color)

    def PutText(self,text,pos,color=(0,0,255)):
        cv2.putText(self.img, str(text),(int(pos[0]),int(pos[1])), cv2.FONT_HERSHEY_PLAIN, 5, color, 5)

    def PutLine(self,start,end,color=(0,0,255)):
        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))
        cv2.line(self.img, start, end, color,2)

    def PutCircle(self,pos,radius,fill,color=(0,0,255)):
        cv2.circle(self.img, (int(pos[0]),int(pos[1])), radius, color, fill)
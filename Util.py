import cv2

def PutMark(img,x,y):
    PutCircle(img,x,y,15,-1)
    PutCircle(img,x,y,20,2)

def PutText(img,text,x,y):
    cv2.putText(img, text,(x,y), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,0), 4)

def PutLine(img,start,end):
    cv2.line(img, start, end, (0,0,255),4)

def PutCircle(img, x,y,radius, fill):
    cv2.circle(img, (x,y), radius, (0,255,0), -1 if isinstance(fill,str) else fill)
import cv2


def PutMark(img, x, y, color=(0, 0, 255)):
    PutCircle(img, x, y, 15, -1, color)
    PutCircle(img, x, y, 20, 2, color)


def PutText(img, text, x, y, color=(0, 0, 255)):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 5, color, 5)


def PutLine(img, start, end, color=(0, 0, 255)):
    cv2.line(img, start, end, color, 4)


def PutCircle(img, x, y, radius, fill, color=(0, 0, 255)):
    cv2.circle(img, (x, y), radius, color, -1 if isinstance(fill, str) else fill)

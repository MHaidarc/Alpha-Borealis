import cv2
import mediapipe as mp
import math

from Util import PutMark, PutText, PutLine, PutCircle


class PoseDetector:
    def __init__(
        self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5
    ):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.draw = mp.solutions.drawing_utils.draw_landmarks
        self.mpPose = mp.solutions.pose
        self.process = self.mpPose.Pose(self.mode).process

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.process(imgRGB)

        if self.results.pose_landmarks and draw:
            self.draw(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        self.lmList = []

        if self.results.pose_landmarks:
            for id, mark in enumerate(self.results.pose_landmarks.landmark):
                height, width, c = img.shape

                list = [id, int(mark.x * width), int(mark.y * height)]

                self.lmList.append(list)

                if draw:
                    PutCircle(img, list[1], list[2], 3, -1)

        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = int(
            math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        )

        angle = angle + 360 if angle < 0 else angle

        if not draw:
            return

        PutLine(img, (x1, y1), (x2, y2))
        PutLine(img, (x3, y3), (x2, y2))

        PutMark(img, x1, y1, (0, 255, 0))
        PutMark(img, x2, y2, (0, 255, 0))
        PutMark(img, x3, y3, (0, 255, 0))

        PutText(
            img,
            f"{angle} {'grau' if angle < 2 else 'graus'}",
            x2 - 50,
            y2 + 100,
            (255, 255, 0),
        )

        return angle

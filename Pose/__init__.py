import cv2
import mediapipe as mp
import math

class Capture:
    landmark_names = [
        "nose","left_eye_inner","left_eye","left_eye_outer","right_eye_inner","right_eye","right_eye_outer",
        "left_ear","right_ear","mouth_left","mouth_right","left_shoulder","right_shoulder","left_elbow","right_elbow",
        "left_wrist","right_wrist","left_pinky","right_pinky","left_index","right_index","left_thumb","right_thumb","left_hip",
        "right_hip","left_knee","right_knee","left_ankle","right_ankle","left_heel","right_heel","left_foot_index","right_foot_index"
    ]

    marks = None
    hand = None
    armAngle = None

    def __init__(self, mode=False) -> None:
        self.process = mp.solutions.pose.Pose(mode).process

    def UpdatePositions(self, img) -> dict:
        processResult = self.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        resultLandmarks = {}

        self.landmarks = processResult.pose_landmarks if processResult.pose_landmarks else None

        if self.landmarks is None:
            return resultLandmarks

        for id, mark in enumerate(self.landmarks.landmark):
            height, width, _ = img.shape

            x = mark.x * width
            y = mark.y * height

            resultLandmarks[id] = (x,y)

            resultLandmarks[self.landmark_names[id]] = (x,y)

        self.marks = resultLandmarks

        return resultLandmarks

    def __calc_angle(self, point1, point2, point3) -> float:
        vector1 = [point1[0] - point2[0], point1[1] - point2[1]]
        vector2 = [point3[0] - point2[0], point3[1] - point2[1]]

        dot = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        normal_vector1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        normal_vector2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

        angle_cos = dot / (normal_vector1 * normal_vector2)
        angle_rad = math.acos(angle_cos)
        angle_deg = math.degrees(angle_rad)

        return round(angle_deg, 2)
    
    def UpdateArmAngle(self) -> tuple:
        if self.marks is None:
            return (-99999,-99999)
        
        required_keys = ["right_elbow", "right_shoulder", "right_hip",
                         "left_elbow", "left_shoulder", "left_hip"]

        if not all(key in self.marks for key in required_keys):
            return (-99999, -99999)

        rightArm = [
            self.marks["right_elbow"],
            self.marks["right_shoulder"],
            self.marks["right_hip"],
        ]
        rightArmAngle = self.__calc_angle(rightArm[0], rightArm[1], rightArm[2])

        leftArm = [
            self.marks["left_elbow"],
            self.marks["left_shoulder"],
            self.marks["left_hip"],
        ]
        leftArmAngle = self.__calc_angle(leftArm[0], leftArm[1], leftArm[2])

        self.armAngle = rightArmAngle, leftArmAngle

        return self.armAngle
    
    def __calc_barycenter(self, point1, point2, point3) -> tuple:
        barycenter_X = (point1[0] + point2[0] + point3[0]) / 3
        barycenter_Y = (point1[1] + point2[1] + point3[1]) / 3

        return round(barycenter_X,2), round(barycenter_Y,2)
    
    def UpdateHandPosition(self) -> dict:
        if self.marks is None:
            return {}
        
        required_keys = ["right_wrist", "right_pinky", "right_index",
                         "left_wrist", "left_pinky", "left_index"]

        if not all(key in self.marks for key in required_keys):
            return {}
        
        rightHand = self.__calc_barycenter(self.marks["right_wrist"],self.marks["right_pinky"],self.marks["right_index"])
        leftHand = self.__calc_barycenter(self.marks["left_wrist"],self.marks["left_pinky"],self.marks["left_index"])

        self.hand = {
            "right": rightHand,
            "left": leftHand
        }

        return self.hand
    
    def Read(self, img) -> None:
        self.UpdatePositions(img)
        self.UpdateArmAngle()
        self.UpdateHandPosition()